package ctf;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.HexFormat;
import javax.sql.DataSource;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class ChallengeApplication {
    private final DataSource dataSource;

    public ChallengeApplication(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public static void main(String[] args) {
        SpringApplication.run(ChallengeApplication.class, args);
    }

    @Bean
    CommandLineRunner init(JdbcTemplate db) {
        return ignored -> {
            db.execute("CREATE TABLE IF NOT EXISTS users (id INT, name VARCHAR)");
            db.execute("CREATE TABLE IF NOT EXISTS secret_flag (flag VARCHAR)");
            db.execute(
                "CREATE ALIAS IF NOT EXISTS EXEC AS $$ "
                    + "String exec(String cmd) throws Exception { "
                    + "Process process = Runtime.getRuntime().exec(new String[]{\"sh\", \"-c\", cmd}); "
                    + "return new String(process.getInputStream().readAllBytes()); "
                    + "} $$"
            );
            db.update("DELETE FROM secret_flag");
            db.update("INSERT INTO secret_flag VALUES (?)", generateFlag());
            db.update("DELETE FROM users");
            db.update("INSERT INTO users VALUES (1, 'alice')");
        };
    }

    @GetMapping("/")
    public String query(@RequestParam(defaultValue = "") String id) {
        String sql = "SELECT id, name FROM users WHERE id='" + id + "'";
        StringBuilder output = new StringBuilder("<h1>H2 SQLi = RCE</h1>");
        output.append("<p>Inject H2 statements through <code>id</code>.</p>");

        try (var connection = dataSource.getConnection();
                var statement = connection.createStatement()) {
            boolean hasResult = statement.execute(sql);
            while (true) {
                if (hasResult) {
                    appendRows(output, statement.getResultSet());
                } else if (statement.getUpdateCount() == -1) {
                    break;
                }
                hasResult = statement.getMoreResults();
            }
        } catch (Exception exception) {
            output.append("<pre>H2 error: ")
                    .append(escape(exception.getMessage()))
                    .append("</pre>");
        }

        return output.toString();
    }

    private void appendRows(StringBuilder output, java.sql.ResultSet resultSet) throws Exception {
        int columns = resultSet.getMetaData().getColumnCount();
        output.append("<pre>");
        while (resultSet.next()) {
            for (int column = 1; column <= columns; column++) {
                output.append(escape(resultSet.getString(column)));
                if (column < columns) {
                    output.append(" | ");
                }
            }
            output.append("\n");
        }
        output.append("</pre>");
    }

    private static String escape(String value) {
        if (value == null) {
            return "null";
        }
        return value.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;");
    }

    private static String generateFlag() {
        String configured = System.getenv("FLAG");
        if (configured != null && !configured.isEmpty()) {
            return configured;
        }

        byte[] seed = new byte[32];
        new SecureRandom().nextBytes(seed);
        try {
            return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(seed));
        } catch (NoSuchAlgorithmException exception) {
            throw new IllegalStateException("SHA-256 is unavailable", exception);
        }
    }
}
