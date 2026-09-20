package main

import (
 "database/sql"
 "fmt"
 "html"
 "net/http"
 "os"
 "os/exec"
 "path/filepath"
 _ "modernc.org/sqlite"
)

var db *sql.DB
func main() {
 var err error; db, err = sql.Open("sqlite", "/tmp/challenge.db"); if err != nil { panic(err) }
 db.Exec("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT); CREATE TABLE IF NOT EXISTS secret_flag (flag TEXT)")
 db.Exec("DELETE FROM secret_flag"); db.Exec("INSERT INTO secret_flag VALUES (?)", env("FLAG", "vladilk{local-sqli-lfi-rce}")); db.Exec("INSERT INTO users VALUES (1,'alice')")
 http.HandleFunc("/", handler); http.ListenAndServe(":80", nil)
}
func handler(w http.ResponseWriter, r *http.Request) {
 id := r.URL.Query().Get("id"); page := r.URL.Query().Get("page"); command := r.URL.Query().Get("c")
 out := "<h1>Go SQLi + LFI = RCE</h1><p>Use <code>id</code> for SQLi, then <code>page</code> for local inclusion.</p>"
 if id != "" { sqlText := "SELECT id,name FROM users WHERE id='" + id + "'"; rows, err := db.Query(sqlText); if err != nil { out += "<pre>SQLite error: " + html.EscapeString(err.Error()) + "</pre>" } else { defer rows.Close(); out += "<pre>query: " + html.EscapeString(sqlText) + "\n"; for rows.Next() { var i int; var name string; rows.Scan(&i, &name); out += fmt.Sprintf("%d %s\n", i, html.EscapeString(name)) }; out += "</pre>" } }
 if page != "" { data, err := os.ReadFile(filepath.Clean(page)); if err != nil { out += "<pre>include error: " + html.EscapeString(err.Error()) + "</pre>" } else { out += "<pre>included file:\n" + html.EscapeString(string(data)) + "</pre>" } }
 if command != "" { data, err := exec.Command("sh", "-c", command).CombinedOutput(); out += "<pre>command:\n" + html.EscapeString(string(data)); if err != nil { out += html.EscapeString(err.Error()) }; out += "</pre>" }
 fmt.Fprint(w, out)
}
func env(key, fallback string) string { if value := os.Getenv(key); value != "" { return value }; return fallback }
