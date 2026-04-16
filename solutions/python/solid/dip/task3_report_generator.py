from abc import ABC, abstractmethod


class Renderer(ABC):
    @abstractmethod
    def render(self, content: str) -> str:
        pass


class PdfRenderer(Renderer):
    def render(self, content: str) -> str:
        return f"[PDF] {content}"


class HtmlRenderer(Renderer):
    def render(self, content: str) -> str:
        return f"<h1>{content}</h1>"


class ReportGenerator:
    def __init__(self, renderer: Renderer):
        self.renderer = renderer

    def generate(self, data: str) -> str:
        content = f"Отчет: {data}"
        return self.renderer.render(content)


if __name__ == "__main__":
    pdf_generator = ReportGenerator(PdfRenderer())
    html_generator = ReportGenerator(HtmlRenderer())

    print(pdf_generator.generate("Продажи за март"))
    print(html_generator.generate("Продажи за март"))
