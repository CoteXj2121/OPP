from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from fnmatch import fnmatch


# Task 1
class ExprNode(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


@dataclass
class NumberNode(ExprNode):
    value: float

    def accept(self, visitor):
        return visitor.visit_number(self)


@dataclass
class VariableNode(ExprNode):
    name: str

    def accept(self, visitor):
        return visitor.visit_variable(self)


@dataclass
class UnaryOpNode(ExprNode):
    operator: str
    operand: ExprNode

    def accept(self, visitor):
        return visitor.visit_unary(self)


@dataclass
class BinaryOpNode(ExprNode):
    operator: str
    left: ExprNode
    right: ExprNode

    def accept(self, visitor):
        return visitor.visit_binary(self)


class EvalVisitor:
    def __init__(self, variables: dict[str, float]):
        self.variables = variables

    def visit_number(self, node: NumberNode):
        return node.value

    def visit_variable(self, node: VariableNode):
        return self.variables[node.name]

    def visit_unary(self, node: UnaryOpNode):
        value = node.operand.accept(self)
        return -value if node.operator == "-" else value

    def visit_binary(self, node: BinaryOpNode):
        left = node.left.accept(self)
        right = node.right.accept(self)
        operations = {
            "+": left + right,
            "-": left - right,
            "*": left * right,
            "/": left / right,
        }
        return operations[node.operator]


class PrintVisitor:
    def visit_number(self, node: NumberNode):
        return str(node.value)

    def visit_variable(self, node: VariableNode):
        return node.name

    def visit_unary(self, node: UnaryOpNode):
        return f"({node.operator}{node.operand.accept(self)})"

    def visit_binary(self, node: BinaryOpNode):
        return f"({node.left.accept(self)} {node.operator} {node.right.accept(self)})"


class RpnVisitor:
    def visit_number(self, node: NumberNode):
        return str(node.value)

    def visit_variable(self, node: VariableNode):
        return node.name

    def visit_unary(self, node: UnaryOpNode):
        return f"{node.operand.accept(self)} {node.operator}"

    def visit_binary(self, node: BinaryOpNode):
        return f"{node.left.accept(self)} {node.right.accept(self)} {node.operator}"


# Task 2
class CartElement(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


@dataclass
class SimpleProduct(CartElement):
    name: str
    price: float

    def accept(self, visitor):
        return visitor.visit_simple_product(self)


@dataclass
class BundleProduct(CartElement):
    name: str
    items: list[SimpleProduct]

    def accept(self, visitor):
        return visitor.visit_bundle_product(self)


@dataclass
class DigitalProduct(CartElement):
    name: str
    price: float

    def accept(self, visitor):
        return visitor.visit_digital_product(self)


@dataclass
class GiftCard(CartElement):
    amount: float

    def accept(self, visitor):
        return visitor.visit_gift_card(self)


class PriceCalculator:
    def visit_simple_product(self, node: SimpleProduct):
        return node.price

    def visit_bundle_product(self, node: BundleProduct):
        return sum(item.price for item in node.items) * 0.9

    def visit_digital_product(self, node: DigitalProduct):
        return node.price

    def visit_gift_card(self, node: GiftCard):
        return node.amount


class ShippingCalculator:
    def visit_simple_product(self, node: SimpleProduct):
        return 10

    def visit_bundle_product(self, node: BundleProduct):
        return 15

    def visit_digital_product(self, node: DigitalProduct):
        return 0

    def visit_gift_card(self, node: GiftCard):
        return 0


class TaxCalculator:
    def visit_simple_product(self, node: SimpleProduct):
        return node.price * 0.2

    def visit_bundle_product(self, node: BundleProduct):
        return sum(item.price for item in node.items) * 0.15

    def visit_digital_product(self, node: DigitalProduct):
        return node.price * 0.1

    def visit_gift_card(self, node: GiftCard):
        return 0


# Task 3
class FsNode(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


@dataclass
class File(FsNode):
    name: str
    content: str
    permissions: str

    def accept(self, visitor):
        return visitor.visit_file(self)


@dataclass
class Directory(FsNode):
    name: str
    children: list[FsNode] = field(default_factory=list)

    def accept(self, visitor):
        return visitor.visit_directory(self)


@dataclass
class SymLink(FsNode):
    name: str
    target: File

    def accept(self, visitor):
        return visitor.visit_symlink(self)


class SizeCalculator:
    def visit_file(self, node: File):
        return len(node.content)

    def visit_directory(self, node: Directory):
        return sum(child.accept(self) for child in node.children)

    def visit_symlink(self, node: SymLink):
        return 0


class SearchVisitor:
    def __init__(self, pattern: str):
        self.pattern = pattern

    def visit_file(self, node: File):
        return [node.name] if fnmatch(node.name, self.pattern) else []

    def visit_directory(self, node: Directory):
        results = [node.name] if fnmatch(node.name, self.pattern) else []
        for child in node.children:
            results.extend(child.accept(self))
        return results

    def visit_symlink(self, node: SymLink):
        return [node.name] if fnmatch(node.name, self.pattern) else []


class PermissionsAuditor:
    def visit_file(self, node: File):
        return [node.name] if "777" in node.permissions else []

    def visit_directory(self, node: Directory):
        results = []
        for child in node.children:
            results.extend(child.accept(self))
        return results

    def visit_symlink(self, node: SymLink):
        return []


class DuplicateFinder:
    def __init__(self):
        self.by_content: dict[str, list[str]] = {}

    def visit_file(self, node: File):
        self.by_content.setdefault(node.content, []).append(node.name)
        return self.by_content

    def visit_directory(self, node: Directory):
        for child in node.children:
            child.accept(self)
        return {content: names for content, names in self.by_content.items() if len(names) > 1}

    def visit_symlink(self, node: SymLink):
        return self.by_content


# Task 4
class DomNode(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


@dataclass
class TextNode(DomNode):
    text: str

    def accept(self, visitor):
        return visitor.visit_text(self)


@dataclass
class CommentNode(DomNode):
    text: str

    def accept(self, visitor):
        return visitor.visit_comment(self)


@dataclass
class ElementNode(DomNode):
    tag: str
    attributes: dict[str, str]
    children: list[DomNode]

    def accept(self, visitor):
        return visitor.visit_element(self)


class HtmlRenderer:
    def visit_text(self, node: TextNode):
        return node.text

    def visit_comment(self, node: CommentNode):
        return f"<!--{node.text}-->"

    def visit_element(self, node: ElementNode):
        attrs = " ".join(f'{key}="{value}"' for key, value in node.attributes.items())
        attrs = f" {attrs}" if attrs else ""
        inner = "".join(child.accept(self) for child in node.children)
        return f"<{node.tag}{attrs}>{inner}</{node.tag}>"


class TextExtractor:
    def visit_text(self, node: TextNode):
        return node.text

    def visit_comment(self, node: CommentNode):
        return ""

    def visit_element(self, node: ElementNode):
        return " ".join(filter(None, (child.accept(self) for child in node.children)))


class LinkCollector:
    def visit_text(self, node: TextNode):
        return []

    def visit_comment(self, node: CommentNode):
        return []

    def visit_element(self, node: ElementNode):
        links = []
        if "href" in node.attributes:
            links.append(node.attributes["href"])
        for child in node.children:
            links.extend(child.accept(self))
        return links


class WordCounter:
    def visit_text(self, node: TextNode):
        return len(node.text.split())

    def visit_comment(self, node: CommentNode):
        return 0

    def visit_element(self, node: ElementNode):
        return sum(child.accept(self) for child in node.children)


# Task 5
class CodeNode(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


@dataclass
class FunctionCall(CodeNode):
    name: str

    def accept(self, visitor):
        return visitor.visit_function_call(self)


@dataclass
class Assignment(CodeNode):
    target: str
    value: str

    def accept(self, visitor):
        return visitor.visit_assignment(self)


@dataclass
class ReturnStatement(CodeNode):
    value: str

    def accept(self, visitor):
        return visitor.visit_return(self)


@dataclass
class IfStatement(CodeNode):
    condition: str
    body: list[CodeNode]

    def accept(self, visitor):
        return visitor.visit_if(self)


@dataclass
class ForLoop(CodeNode):
    variable: str
    iterable: str
    body: list[CodeNode]

    def accept(self, visitor):
        return visitor.visit_for(self)


@dataclass
class FunctionDef(CodeNode):
    name: str
    docstring: str | None
    body: list[CodeNode]

    def accept(self, visitor):
        return visitor.visit_function_def(self)


@dataclass
class ClassDef(CodeNode):
    name: str
    docstring: str | None
    body: list[CodeNode]

    def accept(self, visitor):
        return visitor.visit_class_def(self)


class ComplexityAnalyzer:
    def __init__(self):
        self.complexity = 1

    def visit_function_call(self, node: FunctionCall):
        return self.complexity

    def visit_assignment(self, node: Assignment):
        return self.complexity

    def visit_return(self, node: ReturnStatement):
        return self.complexity

    def visit_if(self, node: IfStatement):
        self.complexity += 1
        for child in node.body:
            child.accept(self)
        return self.complexity

    def visit_for(self, node: ForLoop):
        self.complexity += 1
        for child in node.body:
            child.accept(self)
        return self.complexity

    def visit_function_def(self, node: FunctionDef):
        for child in node.body:
            child.accept(self)
        return self.complexity

    def visit_class_def(self, node: ClassDef):
        for child in node.body:
            child.accept(self)
        return self.complexity


class DependencyCollector:
    def __init__(self):
        self.dependencies: set[str] = set()

    def visit_function_call(self, node: FunctionCall):
        self.dependencies.add(node.name)
        return self.dependencies

    def visit_assignment(self, node: Assignment):
        return self.dependencies

    def visit_return(self, node: ReturnStatement):
        return self.dependencies

    def visit_if(self, node: IfStatement):
        for child in node.body:
            child.accept(self)
        return self.dependencies

    def visit_for(self, node: ForLoop):
        for child in node.body:
            child.accept(self)
        return self.dependencies

    def visit_function_def(self, node: FunctionDef):
        for child in node.body:
            child.accept(self)
        return self.dependencies

    def visit_class_def(self, node: ClassDef):
        for child in node.body:
            child.accept(self)
        return self.dependencies


class DocstringChecker:
    def __init__(self):
        self.missing: list[str] = []

    def visit_function_call(self, node: FunctionCall):
        return self.missing

    def visit_assignment(self, node: Assignment):
        return self.missing

    def visit_return(self, node: ReturnStatement):
        return self.missing

    def visit_if(self, node: IfStatement):
        for child in node.body:
            child.accept(self)
        return self.missing

    def visit_for(self, node: ForLoop):
        for child in node.body:
            child.accept(self)
        return self.missing

    def visit_function_def(self, node: FunctionDef):
        if not node.docstring:
            self.missing.append(f"Function {node.name} has no docstring")
        for child in node.body:
            child.accept(self)
        return self.missing

    def visit_class_def(self, node: ClassDef):
        if not node.docstring:
            self.missing.append(f"Class {node.name} has no docstring")
        for child in node.body:
            child.accept(self)
        return self.missing


if __name__ == "__main__":
    print("Task 1")
    ast = BinaryOpNode("*", BinaryOpNode("+", NumberNode(2), VariableNode("x")), UnaryOpNode("-", NumberNode(3)))
    print(ast.accept(EvalVisitor({"x": 4})))
    print(ast.accept(PrintVisitor()))
    print(ast.accept(RpnVisitor()))
    print("-" * 40)

    print("Task 2")
    items: list[CartElement] = [
        SimpleProduct("Book", 100),
        BundleProduct("Set", [SimpleProduct("Pen", 50), SimpleProduct("Pencil", 30)]),
        DigitalProduct("E-book", 70),
        GiftCard(500),
    ]
    print([item.accept(PriceCalculator()) for item in items])
    print([item.accept(ShippingCalculator()) for item in items])
    print([item.accept(TaxCalculator()) for item in items])
    print("-" * 40)

    print("Task 3")
    root = Directory("root", [File("a.txt", "hello", "644"), File("b.txt", "hello", "777"), SymLink("link", File("c.txt", "data", "644"))])
    print(root.accept(SizeCalculator()))
    print(root.accept(SearchVisitor("*.txt")))
    print(root.accept(PermissionsAuditor()))
    print(root.accept(DuplicateFinder()))
    print("-" * 40)

    print("Task 4")
    dom = ElementNode("a", {"href": "https://example.com"}, [TextNode("Hello world"), CommentNode("note")])
    print(dom.accept(HtmlRenderer()))
    print(dom.accept(TextExtractor()))
    print(dom.accept(LinkCollector()))
    print(dom.accept(WordCounter()))
    print("-" * 40)

    print("Task 5")
    code_ast = FunctionDef(
        "process",
        None,
        [
            Assignment("x", "1"),
            IfStatement("x > 0", [FunctionCall("print")]),
            ForLoop("i", "items", [FunctionCall("handle")]),
            ReturnStatement("x"),
        ],
    )
    print(code_ast.accept(ComplexityAnalyzer()))
    print(code_ast.accept(DependencyCollector()))
    print(code_ast.accept(DocstringChecker()))
