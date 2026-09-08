# src/q.cr

module Q
  VERSION = "0.1.0"

  def self.run(source : String)
    tokens = Lexer.tokenize(source)
    ast = Parser.parse(tokens)
    Runtime.execute(ast)
  end
end
