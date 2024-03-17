import sys
import os

FILE_NAME = "QuizGUI.pro"

def parseSlot(line: str) -> str:
    '''Parses line and returns the function name for the slot inside SLOT().
    
    Will return empty str if no slot could be parsed'''
    try:
        index = line.rindex("SLOT")
        functName = line[index:-1].split("(")[1]
        return functName + "()"
    except ValueError or IndexError:
        # rindex() fails to find SLOT
        return ""

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("no filename given")
        exit(1)
    filename = args[1]
    doWrite = False

    cppFileName = f"{filename}.cpp"
    
    # Edit the .pro file
    with open(FILE_NAME, "r+") as file:
        # read lines
        contents = file.read()
        sections = contents.split("\n\n")
        # skip to sources
        sources = sections[1]
        # split sources into lines
        source_lines = sources.split("\n")
        existsCPP = False
        for i in range(2, len(source_lines)):
            # file found
            if source_lines[i].find(cppFileName) != -1:
                existsCPP = True
                break 
        # need to add it to sources
        if not existsCPP:
            oldLastLine = source_lines[-1]
            newLastLine = f"\tsrc/{cppFileName}"
            source_lines[-1] = f"{oldLastLine} \\"
            source_lines.append(newLastLine)
            sections[1] = "\n".join(source_lines)
            doWrite = True
        
        # Now check Headers
        headers = sections[2]
        header_lines = headers.split("\n")
        existsHFile = False
        for i in range(2, len(header_lines)):
            # file found
            if header_lines[i].find(filename) != -1:
                existsHFile = True
                break
        if not existsHFile:
            oldLastLine = header_lines[-1]
            newLastLine = f"\tsrc/{filename}.h"
            header_lines[-1] = f"{oldLastLine} \\"
            header_lines.append(newLastLine)
            sections[2] = "\n".join(header_lines)
            doWrite = True # think this is redundant but just to be safe
        
        # Now rejoin sections a rewrite to file
        if doWrite:
            file.seek(0)
            new_contents = "\n\n".join(sections)
            file.write(new_contents)
            file.truncate() # new contents will never be shorter but just in case
            print(f"Source/Headers added to {FILE_NAME}")
        else:
            print(f"No changes made to {FILE_NAME}")

    # parse ui_filename.h for things to write to the filename.h file
    toWrite_list = ["placeholder", f'#include "ui_{filename}.h"']
    if not os.path.exists(f"GeneratedFiles/ui_{filename}.h"):
        print(f"ERROR: unable to parse ui_{filename}.h\nCould not generate cpp and h files.")
        exit(1)

    with open(f"GeneratedFiles/ui_{filename}.h", "r") as ui_file:
        # skip until void setupUi
        current_line = ui_file.readline()
        TARGET = "    void setupUi"
        while not current_line.startswith(TARGET):
            current_line = ui_file.readline()
        
        # parse the parent class
        parent_class = current_line.rsplit(" ", 1)[0][len(TARGET)+1:] # DIGSUSTING>>but it should work
        toWrite_list[0] = f"#include <QtWidgets/{parent_class}>"
        toWrite_list.append("")
        toWrite_list.append(f"class {filename} : public {parent_class}")
        toWrite_list.append("{")
        toWrite_list.append("\tQ_OBJECT")
        toWrite_list.append("private:")
        toWrite_list.append("")
        toWrite_list.append("public:")
        toWrite_list.append(f"\t{filename}({parent_class} *parent = Q_NULLPTR);")
        toWrite_list.append("\tvoid initialize();")
        toWrite_list.append("")

        # skip ahead in file until slots part
        TARGET = "    QObject::connect"
        current_line = ui_file.readline()
        while not current_line.startswith(TARGET) and not current_line.startswith("    }"):
            current_line = ui_file.readline()

        if not current_line.startswith("    }"):
            toWrite_list.append("\tpublic slots:")

        # parse each slot
        while current_line.startswith(TARGET):
            slot_name = parseSlot(current_line)
            toWrite_list.append(f"\tvoid {slot_name};")
            current_line = ui_file.readline()

        # Add ui variable last
        TARGET = "    class "
        toWrite_list.append("private:")
        while not current_line.startswith(TARGET):
            current_line = ui_file.readline()
        
        class_name = current_line.split(":")[0][len(TARGET):]
        toWrite_list.append(f"\tUi::{class_name} ui;")
        toWrite_list.append("};")


    # Generate the .cpp and .h files
    alreadyExists = os.path.exists(f"src/{filename}.h")
    if not alreadyExists:
        # SUPER easy just go line by line in toWrite_lsit and write to file
        with open(f"src/{filename}.h", "w") as h_file:
            for line in toWrite_list:
                h_file.write(line + "\n")

        # write cpp file
        with open(f"src/{filename}.h", "r") as h_file:
            with open(f"src/{filename}.cpp", "w") as cpp_file:
                # write header include
                cpp_file.write(f'#include "{filename}.h"\n\n')

                # define 
                current_line = h_file.readline()
                # skip to methods
                while current_line != "public:\n":
                    current_line = h_file.readline()
                
                # Write methods to cpp file
                current_line = h_file.readline()
                # Write constructor first
                cpp_file.write(f"{filename}::{filename}(QWidget *parent)\n\t: {parent_class}(parent)\n" + "{\n\t\n}\n\n")

                current_line = h_file.readline()

                while current_line != "\n" and current_line != "private:\n":
                    try:
                        tokens = current_line.lstrip("\t").rstrip("\n").split("(", 1)
                        tokens2 = tokens[0].split(" ")
                        parameters = tokens[1]
                        cpp_file.write(f"{tokens2[0]} {filename}::{tokens2[1]}({parameters[:-1]}\n" + "{\n\t\n}\n\n")
                    except IndexError:
                        print("Could not parse:\n"+current_line)
                    current_line = h_file.readline()
        
    else:
        # SUPER NOT easy, read file contents first and then go line by line comparing to toWrite_list
        KEYWORD_LIST = ["#inc", "class", "private:", "public:", "\tpublic slots:", "private:"]
        with open(f"src/{filename}.h", "r") as h_file:
            h_contents = h_file.read().split("\n")
        H_CONT_MAX = len(h_contents)
        old_ptr = 0
        TO_WRITE_MAX = len(toWrite_list)
        new_ptr = 0
        with open(f"src/{filename}.h", "w") as h_file:

            for keyword in KEYWORD_LIST:

                backup_ptr = new_ptr
                exists = True
                while not toWrite_list[new_ptr].startswith(keyword):
                    new_ptr += 1
                    # keyword not found, cont to next one
                    if new_ptr >= TO_WRITE_MAX:
                        new_ptr = backup_ptr
                        exists = False
                        break
                
                if exists:

                    # write everything before keyword
                    while not h_contents[old_ptr].startswith(keyword):
                        h_file.write(h_contents[old_ptr] + "\n")
                        old_ptr += 1 # inc ptr

                    # new_ptr and old_ptr should be pointing at same thing now
                    while toWrite_list[new_ptr].startswith(keyword):
                        h_file.write(toWrite_list[new_ptr] + "\n")
                        old_ptr += toWrite_list[new_ptr] == h_contents[old_ptr] # only inc old if they're same
                        new_ptr += 1

                    
            # finish writing rest of old contents
            while old_ptr < H_CONT_MAX - 1:
                h_file.write(h_contents[old_ptr] + "\n")
                old_ptr += 1
            if h_contents[old_ptr] != "":
                h_file.write(h_contents[old_ptr])
        
        # Check cpp file
        with open(f"src/{filename}.cpp", "r") as cpp_file:
            cpp_contents = cpp_file.read().split("\n")
        if cpp_contents[-1] == "":
            cpp_contents.pop()
        CPP_CONT_MAX = len(cpp_contents)
        cpp_ptr = 0
        with open(f"src/{filename}.cpp", "w") as cpp_file:
            with open(f"src/{filename}.h", "r") as h_file:
                # skip to public:
                current_line = h_file.readline()
                while not current_line.startswith("public") and current_line != "":
                    current_line = h_file.readline()
                if current_line == "":
                    # reached eof without seeing public:
                    print(f"Could not parse functions. public: not found in {filename}.h\n{filename}.cpp not changed")
                    while cpp_ptr < CPP_CONT_MAX:
                        cpp_file.write(cpp_contents[cpp_ptr] + "\n")
                else:
                    # public found. Begin checking functions
                    while not current_line.startswith("private"):
                        # check for public slots
                        if current_line.lstrip().startswith("public"):
                            current_line = h_file.readline()
                            continue
                        
                        h_tokens = current_line.split("(") # [0] = funct name/type [1] parameters
                        nameType = h_tokens[0].lstrip().split(" ") # [0] = type [1] = name
                        if len(nameType) > 1:
                            # method
                            name = nameType[1]
                            funcType = nameType[0]
                        else:
                            # constructor
                            current_line = h_file.readline()
                            continue
                        cpp_tokens = cpp_contents[cpp_ptr].split("(")
                        # Write until you reach first function
                        while not cpp_tokens[0].endswith(name):
                            cpp_file.write("(".join(cpp_tokens) + "\n")
                            cpp_ptr += 1
                            cpp_tokens = cpp_contents[cpp_ptr].split("(")
                        current_line = h_file.readline()
                    # Write any remaining things
                    while cpp_ptr < CPP_CONT_MAX:
                        cpp_file.write(cpp_contents[cpp_ptr] + "\n")
                        cpp_ptr += 1
                        