# Blockchain/bridge_interface.rb - Q-lang On-Chain Interaction Layer
require 'eth' # Underneath the Ruby wrapper stack
require_relative '../Core/semantic_error'

module AuraEcosystem
  module Blockchain
    class BridgeInterface
      def initialize(provider_url, contract_address)
        @client = Eth::Client.create(provider_url)
        @contract = Eth::Contract.from_abi(
          name: "QSemanticOracle",
          address: contract_address,
          abi: File.read("./etc/abi/oracle.json")
        )
      end

      # Triggers an immutable state transaction based on an Agent's inference
      def relay_agent_inference(agent_id, verified_payload, private_key)
        key = Eth::Key.new(priv: private_key)
        
        # Validates parameters locally using internal schema validation
        unless Q_Lang::Engine.validate_meaning(verified_payload)
          raise SemanticValidationError, "Payload meaning mismatch"
        end

        # Direct trustless dispatch to the smart contract
        tx_hash = @client.transact(
          @contract, 
          "updateSemanticState", 
          agent_id, 
          verified_payload, 
          sender_key: key
        )
        
        return tx_hash
      end
    end
  end
end
