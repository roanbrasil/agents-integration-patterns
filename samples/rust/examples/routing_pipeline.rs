// Pattern: Pipeline
// Three sequential processing stages chained together.

fn fetch(input: String) -> String {
    let result = format!("FETCHED({})", input);
    println!("Stage 1 - Fetch: {}", result);
    result
}

fn transform(input: String) -> String {
    let result = format!("TRANSFORMED({})", input.to_uppercase());
    println!("Stage 2 - Transform: {}", result);
    result
}

fn summarize(input: String) -> String {
    let snippet = &input[..input.len().min(40)];
    let result = format!("SUMMARY: {} ...[condensed]", snippet);
    println!("Stage 3 - Summarize: {}", result);
    result
}

fn main() {
    println!("=== Pipeline Pattern ===\n");

    let input = "quarterly earnings data from finance API".to_string();
    println!("Input: {}\n", input);

    let output = summarize(transform(fetch(input)));

    println!("\nFinal output: {}", output);
}
