use crate::lexer::token::{Token, TokenKind};

pub struct Lexer {
    source: Vec<char>,
    position: usize,
    line: usize,
    column: usize,
}

impl Lexer {
    pub fn new(input: &str) -> Self {
        Self {
            source: input.chars().collect(),
            position: 0,
            line: 1,
            column: 1,
        }
    }

    pub fn tokenize(&mut self) -> Vec<Token> {
        let mut tokens = Vec::new();

        while self.position < self.source.len() {
            let ch = self.source[self.position];

            match ch {
                ' ' | '\t' | '\r' => self.advance(),

                '\n' => {
                    self.advance();
                    self.line += 1;
                    self.column = 1;
                }

                '+' => {
                    tokens.push(self.token(TokenKind::Plus, "+"));
                    self.advance();
                }

                '-' => {
                    tokens.push(self.token(TokenKind::Minus, "-"));
                    self.advance();
                }

                '*' => {
                    tokens.push(self.token(TokenKind::Star, "*"));
                    self.advance();
                }

                '/' => {
                    tokens.push(self.token(TokenKind::Slash, "/"));
                    self.advance();
                }

                '(' => {
                    tokens.push(self.token(TokenKind::LeftParen, "("));
                    self.advance();
                }

                ')' => {
                    tokens.push(self.token(TokenKind::RightParen, ")"));
                    self.advance();
                }

                '{' => {
                    tokens.push(self.token(TokenKind::LeftBrace, "{"));
                    self.advance();
                }

                '}' => {
                    tokens.push(self.token(TokenKind::RightBrace, "}"));
                    self.advance();
                }

                _ if ch.is_ascii_digit() => {
                    tokens.push(self.number());
                }

                _ if is_identifier_start(ch) => {
                    tokens.push(self.identifier());
                }

                _ => {
                    self.advance();
                }
            }
        }

        tokens.push(Token {
            kind: TokenKind::EOF,
            lexeme: String::new(),
            line: self.line,
            column: self.column,
        });

        tokens
    }

    fn token(&self, kind: TokenKind, text: &str) -> Token {
        Token {
            kind,
            lexeme: text.to_string(),
            line: self.line,
            column: self.column,
        }
    }

    fn number(&mut self) -> Token {
        let start = self.position;

        while self.position < self.source.len()
            && self.source[self.position].is_ascii_digit()
        {
            self.advance();
        }

        let text: String = self.source[start..self.position].iter().collect();

        Token {
            kind: TokenKind::Integer,
            lexeme: text,
            line: self.line,
            column: self.column,
        }
    }

    fn identifier(&mut self) -> Token {
        let start = self.position;

        while self.position < self.source.len()
            && is_identifier_continue(self.source[self.position])
        {
            self.advance();
        }

        let text: String = self.source[start..self.position].iter().collect();

        let kind = match text.as_str() {
            "let" => TokenKind::Let,
            "var" => TokenKind::Var,
            "const" => TokenKind::Const,
            "fn" => TokenKind::Fn,
            "if" => TokenKind::If,
            "else" => TokenKind::Else,
            "return" => TokenKind::Return,
            "true" => TokenKind::True,
            "false" => TokenKind::False,
            _ => TokenKind::Identifier,
        };

        Token {
            kind,
            lexeme: text,
            line: self.line,
            column: self.column,
        }
    }

    fn advance(&mut self) {
        self.position += 1;
        self.column += 1;
    }
}

fn is_identifier_start(c: char) -> bool {
    c.is_ascii_alphabetic() || c == '_'
}

fn is_identifier_continue(c: char) -> bool {
    c.is_ascii_alphanumeric() || c == '_'
}
