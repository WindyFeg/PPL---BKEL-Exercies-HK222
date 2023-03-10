# Given the grammar of MP as follows:

# INTLIT: [0-9]+ ;

# INTTYPE: 'integer';

# FLOATTYPE: 'real';

#? and AST classes as follows:

# @class Type():abstract

# @class CompoundType(Type):abstract

# $class UnionType(CompoundType):#firstType:Type,secondType:primType

# $class ArrayType(CompoundType):#indexType:Type,eleType:primType

# @class PrimType(Type):abstract

# $class IntType(PrimType): pass

# $class FloatType(PrimType): pass

# $class RangeType(PrimType): #lowbound:int; highbound:int

# ?Please copy the following class into your answer and modify the bodies of its methods to generate the AST of a MP input?

class ASTGeneration(MPVisitor):

    # program: mptype EOF;
    def visitProgram(self,ctx:MPParser.ProgramContext):
        return self.visit(ctx.mptype())

    # mptype: primtype | arraytype;
    def visitMptype(self,ctx:MPParser.MptypeContext):
        return self.visit(ctx.primtype()) if ctx.primtype() else self.visit(ctx.arraytype())

    # arraytype: arraytype dimen | primtype dimen;
    # real [-3..0][-10..-1] -> primtype dimen dimen
    def visitArraytype(self,ctx:MPParser.ArraytypeContext):
        # !GOD HELP ME
        # *primtype dimen dimen
        # *primtype dimen
        # arraytype != null return Union()
        # return Arraytype(Union(RecallUnion,dimen)) if arraytype != null else Arraytype(dimen)
        return ArrayType(self.visit(ctx.dimen()),self.visit(ctx.mptype())) if ctx.primtype() else ArrayType(self.visit(ctx.dimen()),self.visit(ctx.primtype()))

    # primtype: INTTYPE | FLOATTYPE; 
    def visitPrimtype(self,ctx:MPParser.PrimtypeContext): 
        return IntType() if ctx.INTTYPE() else FloatType()

    # dimen: '[' num '..' num ']';
    def visitDimen(self,ctx:MPParser.DimenContext):
        return RangeType(int(ctx.num(0).getText()),int(ctx.num(1).getText()))

    # num: '-'? INTLIT;
    def visitNum(self,ctx:MPParser.DimenContext):
        return IntLit(int(ctx.INTLIT().getText())) if ctx.getChild(0).getText() != '-' else IntLit(-int(ctx.INTLIT().getText()))


 
