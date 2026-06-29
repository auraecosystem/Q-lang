use std::fmt;

#[derive(Debug, Clone, PartialEq)]
pub enum TokenKind {
    // Special
    EOF,
    Error,

    // Identifiers
    Identifier,

    // Literals
    Integer,
    Float,
    String,
    Char,
    Boolean,
    Null,

    // Keywords
    Let,
    Var,
    Const,

    Fn,
    Return,

    If,
    Else,

    While,
    For,
    Loop,
    Break,
    Continue,

    Match,

    Import,
    Export,
    Module,

    Object,
    Trait,
    Impl,

    Async,
    Await,

    True,
    False,

    // Operators
    Plus,
    Minus,
    Star,
    Slash,
    Percent,

    Assign,

    PlusAssign,
    MinusAssign,
    StarAssign,
    SlashAssign,

    Equal,
    NotEqual,

    Less,
    Greater,
    LessEqual,
    GreaterEqual,

    And,
    Or,
    Not,

    Arrow,

    Dot,
    Comma,
    Colon,
    Semicolon,

    DoubleColon,

    Question,

    // Delimiters
    LeftParen,
    RightParen,

    LeftBrace,
    RightBrace,

    LeftBracket,
    RightBracket,
}

#[derive(Debug, Clone)]
pub struct Token {
    pub kind: TokenKind,
    pub lexeme: String,
    pub line: usize,
    pub column: usize,
}

impl fmt::Display for Token {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "{:?} '{}' ({}:{})",
            self.kind,
            self.lexeme,
            self.line,
            self.column
        )
    }
}
