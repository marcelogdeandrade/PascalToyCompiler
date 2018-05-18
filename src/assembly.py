# My module
class AssemblyCode(object):
    assembly_code = ""

    @staticmethod
    def addLine(text):
        AssemblyCode.assembly_code += "\n"
        AssemblyCode.assembly_code += text

    @staticmethod
    def writeFile(filename):
        with open(filename, 'w') as the_file:
            the_file.write(AssemblyCode.assembly_code)
