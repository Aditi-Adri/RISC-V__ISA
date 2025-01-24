# Aditi Roy Adri 
# RISC-V , 32I

import tkinter as tk
from tkinter import messagebox
import instructions


def parts_instruction(instruction):
    try:
        parts = instruction.replace(",", "").replace("(", " ").replace(")", "").split()
        ins = parts[0]  
        reg_or_imm = parts[1:]  
        return ins, reg_or_imm
    except Exception as e:
        raise ValueError(f"Error parsing instruction: {e}")


def register_to_binary(register):
    try:
        reg_num = int(register[1:])
        return format(reg_num, "05b")
    except:
        raise ValueError(f"Invalid register: {register}")


def immediate_to_binary(immediate, bits):
    imm = int(immediate)
    if imm < 0:
        imm = (1 << bits) + imm
    return format(imm, f"0{bits}b")


def convert_to_machine_code(assembly_instruction):
    try:
        mnemonic, operands = parts_instruction(assembly_instruction)
        instr = instructions.INSTRUCTION_SET.get(mnemonic)

        if not instr:
            raise ValueError(f"Unknown instruction: {mnemonic}")

        opcode = instr["opcode"]
        instr_type = instr["type"]

       
        if instr_type == "R-type":
            rd, rs1, rs2 = operands
            binary = f"{instr['funct7']}{register_to_binary(rs2)}{register_to_binary(rs1)}{instr['funct3']}{register_to_binary(rd)}{opcode}"
        elif instr_type == "I-type":
            if mnemonic[0] == "l" :
                rs2, immediate, rs1 = operands  
                imm_bin = immediate_to_binary(immediate, 12)
                binary = (
                    f"{imm_bin[:7]}"  
                    f"{register_to_binary(rs2)}"  
                    f"{register_to_binary(rs1)}"  
                    f"{instr['funct3']}"  
                    f"{imm_bin[7:]}"  
                    f"{opcode}"
                )
            else :
                rd, rs1, immediate = operands
                binary = f"{immediate_to_binary(immediate, 12)}{register_to_binary(rs1)}{instr['funct3']}{register_to_binary(rd)}{opcode}"
        elif instr_type == "S-type":
            rs2, immediate, rs1 = operands  
            imm_bin = immediate_to_binary(immediate, 12)
            binary = (
                f"{imm_bin[:7]}"  
                f"{register_to_binary(rs2)}"  
                f"{register_to_binary(rs1)}"  
                f"{instr['funct3']}" 
                f"{imm_bin[7:]}"  
                f"{opcode}"
            )
        
        elif instr_type == "B-type":
            rs1, rs2, immediate = operands
            imm_bin = immediate_to_binary(immediate, 13)
            binary = f"{imm_bin[0]}{imm_bin[2:8]}{register_to_binary(rs2)}{register_to_binary(rs1)}{instr['funct3']}{imm_bin[8:12]}{imm_bin[1]}{opcode}"
        elif instr_type == "U-type":
            rd, immediate = operands
            binary = f"{immediate_to_binary(immediate, 20)}{register_to_binary(rd)}{opcode}"
        elif instr_type == "J-type":
            rd, immediate = operands
            imm_bin = immediate_to_binary(immediate, 21)
            binary = f"{imm_bin[0]}{imm_bin[10:20]}{imm_bin[9]}{imm_bin[1:9]}{register_to_binary(rd)}{opcode}"
        else:
            raise ValueError(f"Unsupported instruction type: {instr_type}")

       
        hex_code = hex(int(binary, 2))[2:].zfill(8)  

        return {
            "Assembly": assembly_instruction,
            "Binary": binary,
            "Hexadecimal": hex_code.upper(),
            "Format": instr_type,
        }
    except Exception as e:
        return {"Error": str(e)}


def on_convert_button_click():
    assembly_instruction = entry.get().strip()
    if not assembly_instruction:
        messagebox.showwarning("Input Error", "Please enter an assembly instruction.")
        return
    result = convert_to_machine_code(assembly_instruction)
    display_results(result)


def display_results(result):
    if "Error" in result:
        messagebox.showerror("Error", result["Error"])
    else:
        result_text = f"""
        Assembly Instruction: {result['Assembly']}
        Binary: {result['Binary']}
        Hexadecimal: {result['Hexadecimal']}
        Format: {result['Format']}
        """
        result_label.config(
            text=result_text, fg="#0078d4", font=("Segoe UI", 12, "bold")
        )



root = tk.Tk()
root.title("Assembly to Machine Code Converter")


root.geometry("600x500")
root.config(bg="#e6f7ff")  


title_label = tk.Label(
    root,
    text="RISC-V 32-bit Format",
    font=("Segoe UI", 18, "bold"),
    bg="#e6f7ff",
    fg="#333",
)
title_label.pack(pady=10)


label = tk.Label(
    root,
    text="Enter Assembly Instruction:",
    font=("Segoe UI", 12),
    bg="#e6f7ff",
    fg="#555",
)
label.pack(pady=10)


entry = tk.Entry(
    root,
    font=("Segoe UI", 12),
    width=40,
    borderwidth=2,
    relief="flat",
    bg="#fff",
    fg="#333",
    highlightthickness=1,
    highlightbackground="#ccc",
)
entry.pack(pady=10)


convert_button = tk.Button(
    root,
    text="Convert",
    font=("Segoe UI", 14),
    command=on_convert_button_click,
    bg="#0078d4",
    fg="white",
    relief="flat",
    width=20,
)
convert_button.pack(pady=20)


result_label = tk.Label(
    root, text="", font=("Segoe UI", 12), bg="#e6f7ff", fg="#333", justify="left", anchor="w"
)
result_label.pack(pady=20, padx=20)



def on_button_hover(event):
    convert_button.config(bg="#005a8d")


def on_button_leave(event):
    convert_button.config(bg="#0078d4")


convert_button.bind("<Enter>", on_button_hover)
convert_button.bind("<Leave>", on_button_leave)


root.mainloop()