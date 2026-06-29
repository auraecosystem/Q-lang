#[derive(Debug, Clone, PartialEq)]
pub enum Type {
    Int,
    Float,
    Bool,
    String,
    Char,
    Null,
    Void,

    Array(Box<Type>),

    Map(Box<Type>, Box<Type>),

    Function {
        params: Vec<Type>,
        return_type: Box<Type>,
    },

    Object(String),

    Unknown,
}
