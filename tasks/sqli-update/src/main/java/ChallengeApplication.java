package ctf;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.HexFormat;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class ChallengeApplication {
    private static JdbcTemplate db;

    public static void main(String[] args) {
        SpringApplication.run(ChallengeApplication.class, args);
    }

    @Bean
    CommandLineRunner init(JdbcTemplate template) {
        db = template;
        return ignored -> {
            template.execute(
                "CREATE TABLE IF NOT EXISTS users "
                    + "(id INT PRIMARY KEY, username VARCHAR, email VARCHAR, password VARCHAR)"
            );
            template.execute("CREATE TABLE IF NOT EXISTS secret_flag (flag VARCHAR)");
            template.update("DELETE FROM secret_flag");
            template.update(
                "INSERT INTO secret_flag VALUES (?)",
                generateFlag()
            );
            template.update(
                "MERGE INTO users KEY(id) VALUES "
                    + "(1,'alice','alice@example.test','password')"
            );
        };
    }

    @PostMapping("/")
    public String update(
        @RequestParam(defaultValue = "1") String id,
        @RequestParam(defaultValue = "") String email
    ) {
        String sql = "UPDATE users SET email='" + email + "' WHERE id='" + id + "'";
        try {
            db.execute(sql);
            return "<h1>Spring SQLi UPDATE</h1><pre>"
                + sql
                + "\nupdated</pre>"
                + profile(id);
        } catch (Exception exception) {
            return "<pre>H2 error: " + exception.getMessage() + "</pre>";
        }
    }

    @GetMapping("/")
    public String form(@RequestParam(defaultValue = "1") String id) {
        return "<h1>Spring SQLi UPDATE</h1>"
            + "<form method='post'><input name='id' value='1'>"
            + "<input name='email'><button>Update</button></form>"
            + profile(id);
    }

    private String profile(String id) {
        try {
            return "<pre>" + db.queryForList("SELECT * FROM users WHERE id='" + id + "'") + "</pre>";
        } catch (Exception exception) {
            return "<pre>H2 error: " + exception.getMessage() + "</pre>";
        }
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
