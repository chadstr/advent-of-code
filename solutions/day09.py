def compute_str(program_str, verbose=False):
    program_str = program_str + ',0' * 1000  # Add additional memory
    program = program_str.split(',')
    program = [int(opcode) for opcode in program]
    return compute(program, verbose=verbose)

# Returns opcode_str; paramter modes; and number to increment instruction_pointer by
def parse_first(int_value):
    map_opcode_to_param_num = {'99': 0, '01': 3, '02': 3, '03': 1, '04': 1, '05': 2, '06': 2, '07': 3, '08': 3, '09': 1}
    max_value_str_len = max(map_opcode_to_param_num.values()) + 2  # Two len opcode

    value_str = str(int_value)
    value_str = value_str.zfill(max_value_str_len)  # Pad with leading zeros

    opcode_str = value_str[-2:]

    parameter_modes = value_str[:-2]

    if opcode_str not in map_opcode_to_param_num.keys():
        print(f'ERROR - invalid opcode: {opcode_str}')

    parameter_mode_map = {'0': 'position', '1': 'immediate', '2': 'relative'}
    parameter_modes = [parameter_mode_map[parameter_mode] for parameter_mode in parameter_modes]
    parameter_modes = [] if opcode_str == '99' else parameter_modes[-map_opcode_to_param_num[opcode_str]:]  # Reduce to correct num of param modes for opcode
    parameter_modes = parameter_modes[::-1]  # Reverse mode order

    instruction_pointer_increment = map_opcode_to_param_num[opcode_str] + 1

    return opcode_str, parameter_modes, instruction_pointer_increment


def compute(program, verbose=False):
    program = list(program)

    instruction_pointer = 0
    relative_base = 0

    while instruction_pointer < len(program):
        int_value = program[instruction_pointer]
        opcode_str, parameter_modes, instruction_pointer_increment = parse_first(int_value)
        if verbose:
            print(f'Processing: {opcode_str}')

        if opcode_str == '99':
            print('Exiting (99 code)...')
            return program

        elif opcode_str == '01':
            # Add
            param_mode_1, param_mode_2, param_mode_3 = parameter_modes

            parameter_1 = program[instruction_pointer + 1]
            if param_mode_1 == 'position':
                operand_1 = program[parameter_1] 
            elif param_mode_1 == 'immediate':
                operand_1 = parameter_1
            elif param_mode_1 == 'relative':
                operand_1 = program[relative_base + parameter_1] 
            else:
                print(f'ERROR - invalid parameter mode: {parameter_1}')

            parameter_2 = program[instruction_pointer + 2]
            if param_mode_2 == 'position':
                operand_2 = program[parameter_2] 
            elif param_mode_2 == 'immediate':
                operand_2 = parameter_2
            elif param_mode_2 == 'relative':
                operand_2 = program[relative_base + parameter_2] 
            else:
                print(f'ERROR - invalid parameter mode: {param_mode_2}')

            parameter_3 = program[instruction_pointer + 3]
            if param_mode_3 == 'position':  # Note: since writing to memory, cannot be immediate
                output_address = parameter_3
            elif param_mode_3 == 'relative':
                output_address = relative_base + parameter_3
            else:
                print('ERROR - immediate mode for writing to memory')

            # Perform op
            result = operand_1 + operand_2
            program[output_address] = result
            instruction_pointer += instruction_pointer_increment


        elif opcode_str == '02':
            # Multiply
            param_mode_1, param_mode_2, param_mode_3 = parameter_modes

            parameter_1 = program[instruction_pointer + 1]
            if param_mode_1 == 'position':
                operand_1 = program[parameter_1] 
            elif param_mode_1 == 'immediate':
                operand_1 = parameter_1
            elif param_mode_1 == 'relative':
                operand_1 = program[relative_base + parameter_1] 
            else:
                print(f'ERROR - invalid parameter mode: {parameter_1}')

            parameter_2 = program[instruction_pointer + 2]
            if param_mode_2 == 'position':
                operand_2 = program[parameter_2] 
            elif param_mode_2 == 'immediate':
                operand_2 = parameter_2
            elif param_mode_2 == 'relative':
                operand_2 = program[relative_base + parameter_2] 
            else:
                print(f'ERROR - invalid parameter mode: {param_mode_2}')

            parameter_3 = program[instruction_pointer + 3]
            if param_mode_3 == 'position':  # Note: since writing to memory, cannot be immediate
                output_address = parameter_3
            elif param_mode_3 == 'relative':
                output_address = relative_base + parameter_3
            else:
                print('ERROR - immediate mode while writing to memory')

            # Perform op
            result = operand_1 * operand_2
            program[output_address] = result
            instruction_pointer += instruction_pointer_increment

        elif opcode_str == '03':   
            # Input
            param_mode_1 = parameter_modes[0]

            parameter_1 = program[instruction_pointer + 1]
            if param_mode_1 == 'position':
                output_address = parameter_1
            elif param_mode_1 == 'relative':
                output_address = relative_base + parameter_1
            else:
                print('ERROR - immediate mode while writing to memory')

            user_input = None
            # Keep looping while user_input is None
            while user_input is None:
                user_input = (yield 'input')
            if verbose:
                print(f'Input Received: {user_input}')

            program[output_address] = user_input
            instruction_pointer += instruction_pointer_increment

        elif opcode_str == '04':
            # Output
            param_mode_1 = parameter_modes[0]
            parameter_1 = program[instruction_pointer + 1]
            read_address = parameter_1

            if param_mode_1 == 'position':
                output = program[read_address]
            elif param_mode_1 == 'immediate':
                output = read_address
            elif param_mode_1 == 'relative':
                output = program[relative_base + read_address]
            else:
                print(f'ERROR - invalid parameter mode: {param_mode_1}')

            if verbose:
                print(f'Output: {output}')
            yield output
            instruction_pointer += instruction_pointer_increment

        elif opcode_str == '05':
            # Jump if True
            param_mode_1, param_mode_2 = parameter_modes
            parameter_1 = program[instruction_pointer + 1]
            parameter_2 = program[instruction_pointer + 2]

            if param_mode_1 == 'position':
                operand_1 = program[parameter_1]
            elif param_mode_1 == 'immediate':
                operand_1 = parameter_1
            elif param_mode_1 == 'relative':
                operand_1 = program[relative_base + parameter_1]
            else:
                print(f'ERROR - invalid parameter mode: {param_mode_1}')

            if param_mode_2 == 'position':
                operand_2 = program[parameter_2]
            elif param_mode_2 == 'immediate':
                operand_2 = parameter_2
            elif param_mode_2 == 'relative':
                operand_2 = program[relative_base + parameter_2]
            else:
                print(f'ERROR - invalid parameter mode: {param_mode_2}')

            if operand_1 != 0:
                instruction_pointer = operand_2
            else:
                instruction_pointer += instruction_pointer_increment

        elif opcode_str == '06':
            # Jump if False
            param_mode_1, param_mode_2 = parameter_modes
            parameter_1 = program[instruction_pointer + 1]
            parameter_2 = program[instruction_pointer + 2]

            if param_mode_1 == 'position':
                operand_1 = program[parameter_1]
            elif param_mode_1 == 'immediate':
                operand_1 = parameter_1
            elif param_mode_1 == 'relative':
                operand_1 = program[relative_base + parameter_1]
            else:
                print(f'ERROR - invalid parameter mode: {param_mode_1}')

            if param_mode_2 == 'position':
                operand_2 = program[parameter_2]
            elif param_mode_2 == 'immediate':
                operand_2 = parameter_2
            elif param_mode_2 == 'relative':
                operand_2 = program[relative_base + parameter_2]
            else:
                print(f'ERROR - invalid parameter mode: {param_mode_2}')

            if operand_1 == 0:
                instruction_pointer = operand_2
            else:
                instruction_pointer += instruction_pointer_increment

        elif opcode_str == '07':
            # Less than
            param_mode_1, param_mode_2, param_mode_3 = parameter_modes
            parameter_1 = program[instruction_pointer + 1]
            parameter_2 = program[instruction_pointer + 2]

            if param_mode_1 == 'position':
                operand_1 = program[parameter_1]
            elif param_mode_1 == 'immediate':
                operand_1 = parameter_1
            elif param_mode_1 == 'relative':
                operand_1 = program[relative_base + parameter_1]
            else:
                print(f'ERROR - invalid parameter mode: {param_mode_1}')

            if param_mode_2 == 'position':
                operand_2 = program[parameter_2]
            elif param_mode_2 == 'immediate':
                operand_2 = parameter_2
            elif param_mode_2 == 'relative':
                operand_2 = program[relative_base + parameter_2]
            else:
                print(f'ERROR - invalid parameter mode: {param_mode_2}')

            parameter_3 = program[instruction_pointer + 3]
            output_address = parameter_3
            if param_mode_3 == 'position':
                program[output_address] = 1 if operand_1 < operand_2 else 0
            elif param_mode_3 == 'relative':
                program[relative_base + output_address] = 1 if operand_1 < operand_2 else 0
            else:
                print('ERROR - immediate mode while writing to memory')

            instruction_pointer += instruction_pointer_increment

        elif opcode_str == '08':
            # Equals
            param_mode_1, param_mode_2, param_mode_3 = parameter_modes
            parameter_1 = program[instruction_pointer + 1]
            parameter_2 = program[instruction_pointer + 2]

            if param_mode_1 == 'position':
                operand_1 = program[parameter_1]
            elif param_mode_1 == 'immediate':
                operand_1 = parameter_1
            elif param_mode_1 == 'relative':
                operand_1 = program[relative_base + parameter_1]
            else:
                print(f'ERROR - invalid parameter mode: {param_mode_1}')

            if param_mode_2 == 'position':
                operand_2 = program[parameter_2]
            elif param_mode_2 == 'immediate':
                operand_2 = parameter_2
            elif param_mode_2 == 'relative':
                operand_2 = program[relative_base + parameter_2]
            else:
                print(f'ERROR - invalid parameter mode: {param_mode_2}')

            parameter_3 = program[instruction_pointer + 3]
            output_address = parameter_3

            if param_mode_3 == 'position':
                program[output_address] = 1 if operand_1 == operand_2 else 0
            elif param_mode_3 == 'relative':
                program[relative_base + output_address] = 1 if operand_1 == operand_2 else 0
            else:
                print('ERROR - immediate mode while writing to memory')

            instruction_pointer += instruction_pointer_increment

        elif opcode_str == '09':
            # Relative base offset instruction
            param_mode_1 = parameter_modes[0]

            parameter_1 = program[instruction_pointer + 1]
            if param_mode_1 == 'position':
                operand_1 = program[parameter_1]
            elif param_mode_1 == 'immediate':
                operand_1 = parameter_1
            elif param_mode_1 == 'relative':
                operand_1 = program[relative_base + parameter_1]
            else:
                print(f'ERROR - invalid parameter mode: {param_mode_1}')

            relative_base = relative_base + operand_1
            instruction_pointer += instruction_pointer_increment

        else:
            print('ERROR - invalid opcode')
            return

    print('End of program without 99 code')
    return


puzzle_input = '1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1102,1,3,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1102,26,1,1005,1101,0,24,1019,1102,1,32,1007,1101,0,704,1027,1102,0,1,1020,1101,0,348,1029,1102,28,1,1002,1101,34,0,1016,1102,29,1,1008,1102,1,30,1013,1102,25,1,1012,1101,0,33,1009,1102,1,37,1001,1101,31,0,1017,1101,245,0,1022,1102,39,1,1000,1101,27,0,1011,1102,770,1,1025,1101,0,22,1015,1102,1,1,1021,1101,711,0,1026,1101,20,0,1004,1101,0,23,1018,1101,242,0,1023,1102,21,1,1003,1101,38,0,1010,1101,0,35,1014,1101,0,36,1006,1101,0,357,1028,1102,1,775,1024,109,-3,2102,1,9,63,1008,63,36,63,1005,63,203,4,187,1105,1,207,1001,64,1,64,1002,64,2,64,109,8,21101,40,0,5,1008,1010,41,63,1005,63,227,1106,0,233,4,213,1001,64,1,64,1002,64,2,64,109,16,2105,1,2,1105,1,251,4,239,1001,64,1,64,1002,64,2,64,109,1,21107,41,40,-4,1005,1018,271,1001,64,1,64,1105,1,273,4,257,1002,64,2,64,109,-18,1207,0,21,63,1005,63,295,4,279,1001,64,1,64,1105,1,295,1002,64,2,64,109,-3,1207,0,36,63,1005,63,311,1105,1,317,4,301,1001,64,1,64,1002,64,2,64,109,6,2108,20,-3,63,1005,63,339,4,323,1001,64,1,64,1106,0,339,1002,64,2,64,109,28,2106,0,-7,4,345,1001,64,1,64,1106,0,357,1002,64,2,64,109,-18,1206,4,373,1001,64,1,64,1105,1,375,4,363,1002,64,2,64,109,-6,2107,31,-4,63,1005,63,397,4,381,1001,64,1,64,1105,1,397,1002,64,2,64,109,1,21102,42,1,-1,1008,1011,39,63,1005,63,421,1001,64,1,64,1106,0,423,4,403,1002,64,2,64,109,-2,2108,26,-2,63,1005,63,439,1106,0,445,4,429,1001,64,1,64,1002,64,2,64,109,6,21102,43,1,-5,1008,1011,43,63,1005,63,467,4,451,1105,1,471,1001,64,1,64,1002,64,2,64,109,6,21101,44,0,-3,1008,1019,44,63,1005,63,493,4,477,1105,1,497,1001,64,1,64,1002,64,2,64,109,-9,1206,7,511,4,503,1105,1,515,1001,64,1,64,1002,64,2,64,109,14,1205,-7,531,1001,64,1,64,1106,0,533,4,521,1002,64,2,64,109,-27,1201,0,0,63,1008,63,39,63,1005,63,555,4,539,1105,1,559,1001,64,1,64,1002,64,2,64,109,10,2101,0,-5,63,1008,63,24,63,1005,63,583,1001,64,1,64,1105,1,585,4,565,1002,64,2,64,109,-11,2107,21,5,63,1005,63,601,1105,1,607,4,591,1001,64,1,64,1002,64,2,64,109,10,1208,0,36,63,1005,63,627,1001,64,1,64,1106,0,629,4,613,1002,64,2,64,109,15,21108,45,45,-9,1005,1015,647,4,635,1105,1,651,1001,64,1,64,1002,64,2,64,109,-19,2101,0,-4,63,1008,63,37,63,1005,63,677,4,657,1001,64,1,64,1106,0,677,1002,64,2,64,109,22,1205,-6,695,4,683,1001,64,1,64,1105,1,695,1002,64,2,64,109,-10,2106,0,10,1001,64,1,64,1105,1,713,4,701,1002,64,2,64,109,-9,1201,-8,0,63,1008,63,36,63,1005,63,733,1105,1,739,4,719,1001,64,1,64,1002,64,2,64,109,7,21107,46,47,0,1005,1015,757,4,745,1106,0,761,1001,64,1,64,1002,64,2,64,109,14,2105,1,-5,4,767,1105,1,779,1001,64,1,64,1002,64,2,64,109,-34,2102,1,6,63,1008,63,39,63,1005,63,799,1105,1,805,4,785,1001,64,1,64,1002,64,2,64,109,25,21108,47,49,-4,1005,1016,825,1001,64,1,64,1106,0,827,4,811,1002,64,2,64,109,-6,1208,-8,36,63,1005,63,845,4,833,1106,0,849,1001,64,1,64,1002,64,2,64,109,-10,1202,2,1,63,1008,63,36,63,1005,63,875,4,855,1001,64,1,64,1105,1,875,1002,64,2,64,109,-5,1202,10,1,63,1008,63,30,63,1005,63,895,1106,0,901,4,881,1001,64,1,64,4,64,99,21101,27,0,1,21101,0,915,0,1105,1,922,21201,1,65916,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21101,942,0,0,1105,1,922,21201,1,0,-1,21201,-2,-3,1,21102,1,957,0,1105,1,922,22201,1,-1,-2,1106,0,968,22102,1,-2,-2,109,-3,2105,1,0'


if __name__ == '__main__':
    run = compute_str(puzzle_input)
    next(run)
    print(run.send(2))