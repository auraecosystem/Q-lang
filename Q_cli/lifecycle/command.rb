router.register_slash_command("lifecycle") do |input, context|
  target_file = input.split(" ")[1] # e.g., /lifecycle prototype/.anancondq
  puts "Intercepting object: #{target_file}"
  
  # Links dynamically to the core sequence
  lifecycle = Q_Lang::Runtime::Lifecycle.new(target_file)
  lifecycle.detect
  lifecycle.analyze
  lifecycle.learn
  puts "Object successfully integrated into the semantic ecosystem."
end
