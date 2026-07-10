router.register_slash_command("sync") do |input, context|
  agent_id = input.split(" ")[1]
  puts "Initiating trustless cryptographic state relay for #{agent_id}..."
  
  bridge = AuraEcosystem::Blockchain::BridgeInterface.new(ENV['PROVIDER_URL'], ENV['CONTRACT_ADDR'])
  tx = bridge.relay_agent_inference(agent_id, context.current_payload, ENV['PRIV_KEY'])
  puts "State anchored successfully. Transaction hash: #{tx}"
end

