use crate::ast::Type;

#[derive(Debug, Clone)]
pub enum Expression {

    Integer(i64),

    Float(f64),

    Bool(bool),

    String(String),

    Identifier(String),

    Unary {
        operator: UnaryOperator,
        operand: Box<Expression>,
    },

    Binary {
        left: Box<Expression>,
        operator: BinaryOperator,
        right: Box<Expression>,
    },

    Assignment {
        name: String,
        value: Box<Expression>,
    },

    Call {
        callee: Box<Expression>,
        arguments: Vec<Expression>,
    },

    Member {
        object: Box<Expression>,
        property: String,
    },

    Array(Vec<Expression>),

    Null,
}

#[derive(Debug, Clone)]
pub enum UnaryOperator {
    Negate,
    Not,
}

#[derive(Debug, Clone)]
pub enum BinaryOperator {

    Add,

    Subtract,

    Multiply,

    Divide,

    Modulo,

    Equal,

    NotEqual,

    Less,

    LessEqual,

    Greater,

    GreaterEqual,

    And,

    Or,
}
