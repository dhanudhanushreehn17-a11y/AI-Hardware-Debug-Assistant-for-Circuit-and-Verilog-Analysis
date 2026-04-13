// Sample Verilog Code with Errors
// This file is for testing the AI Hardware Debug Assistant

// ============================================
// Module 1: Counter with errors
// ============================================
module counter_with_errors (
    input clk,
    input rst,
    input enable,
    output reg [7:0] count
);

    // Error 1: Using blocking assignment in always block (should be non-blocking)
    always @(posedge clk) begin
        if (rst)
            count = 0;  // Should be <= not =
        else if (enable)
            count = count + 1;
    end

endmodule

// ============================================
// Module 2: FSM with incomplete case
// ============================================
module fsm_incomplete (
    input clk,
    input rst,
    input [1:0] in,
    output reg [1:0] out
);

    reg [1:0] state;
    
    // Error 2: Incomplete case statement (missing default)
    always @(posedge clk) begin
        if (rst)
            state <= 2'b00;
        else begin
            case (state)
                2'b00: if (in == 2'b01) state <= 2'b01;
                2'b01: if (in == 2'b10) state <= 2'b10;
                2'b10: if (in == 2'b00) state <= 2'b00;
                // Missing default case - potential latch inference
            endcase
        end
    end
    
    // Error 3: out not reset
    always @(*) begin
        case (state)
            2'b00: out = 2'b01;
            2'b01: out = 2'b10;
            2'b10: out = 2'b11;
        endcase
    end

endmodule

// ============================================
// Module 3: Module instantiation with errors
// ============================================
module top_module (
    input clk,
    input rst,
    input [7:0] data_in,
    output [7:0] data_out
);

    wire [7:0] temp;
    
    // Error 4: Missing output port connection
    my_module instance1 (
        .clk(clk),
        .rst(rst),
        .data_in(data_in)
        // Missing .data_out(temp)
    );
    
    assign temp = 8'h00;

endmodule

module my_module (
    input clk,
    input rst,
    input [7:0] data_in,
    output reg [7:0] data_out
);

    always @(posedge clk) begin
        if (rst)
            data_out <= 0;
        else
            data_out <= data_in;
    end

endmodule
