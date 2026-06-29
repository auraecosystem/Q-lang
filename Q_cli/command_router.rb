# Q_cli/command_router.rb - Registering custom slash utilities
module AuraEcosystem
  module CLI
    class CommandRouter
      def initialize
        @custom_commands = {}
        register_defaults
      end

      # Binds a terminal prefix to a specific script execution block
      def register_slash_command(trigger, &block)
        @custom_commands["/#{trigger}"] = block
      end

      def execute(input_line, active_context)
        command = input_line.strip.split(" ").first
        if @custom_commands.has_key?(command)
          @custom_commands[command].call(input_line, active_context)
        else
          puts "Unknown command. Use /help to see valid targets."
        end
      end

      private

      def register_defaults
        register_slash_command("help") { puts "Available paths: /test, /lifecycle, /sync" }
      end
    end
  end
end
