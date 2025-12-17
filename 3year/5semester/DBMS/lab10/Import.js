import fs from "fs";
import readline from "readline";
import postgres from "postgres";

const FILE_PATH = 'D:/OMGTU/OMGTU/3year/5semester/DBMS/lab10/goodreads_books.json';
const POSTGRES_CONNECTION_STRING = 
    "postgres://postgres:123@localhost:5432/lr10";
const BATCH_SIZE = 5000;

const rl = readline.createInterface({
    input: fs.createReadStream(FILE_PATH, { encoding: "utf-8" })
});

const sql = postgres(POSTGRES_CONNECTION_STRING);

let rows = [];
let processedCount = 0;

console.log("Начало импорта...");

for await (const line of rl) {
    try {
        const record = JSON.parse(line);
        rows.push({
            isbn: record.isbn || null,
            title: record.title || null,
            description: record.description || null,
            year: record.publication_year || null,
            rating: record.average_rating || null,
            rating_count: record.ratings_count || null,
            pages: record.num_pages ? parseInt(record.num_pages) : null,
            authors: record.authors ? record.authors.map((a) => parseInt(a.author_id)) || null : null
        });

        if (rows.length >= BATCH_SIZE) {
            await sql`INSERT INTO books ${sql(rows)}`;
            processedCount += rows.length;
            console.log(`Импортировано: ${processedCount} записей`);
            rows = [];
        }
    } catch (e) {
        console.error("Ошибка при обработке строки:", e.message);
    }
}

if (rows.length > 0) {
    await sql`INSERT INTO books ${sql(rows)}`;
    processedCount += rows.length;
    console.log(`Импортировано: ${processedCount} записей`);
}

rl.close();
await sql.end();
console.log("Импорт завершен!");