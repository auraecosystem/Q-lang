use crate::ast::{Expression, Type};

#[derive(Debug, Clone)]
pub enum Statement {

    Let {
        name: String,
        value: Expression,
    },

    Var {
        name: String,
        value: Expression,
    },

    Const {
        name: String,
        value: Expression,
    },

    Function {
        name: String,
        parameters: Vec<Parameter>,
        return_type: Type,
        body: Vec<Statement>,
    },

    Return(Option<Expression>),

    If {
        condition: Expression,
        then_branch: Vec<Statement>,
        else_branch: Vec<Statement>,
    },

    While {
        condition: Expression,
        body: Vec<Statement>,
    },

    Expression(Expression),
}

#[derive(Debug, Clone)]
pub struct Parameter {
    pub name: String,
    pub ty: Type,
}
