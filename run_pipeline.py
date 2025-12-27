import argparse, json, os
from agents.parser import ParserAgent
from agents.question_generator import QuestionGeneratorAgent
from agents.template_renderer import TemplateRendererAgent
from exporters.json_exporter import JSONExporterAgent

def load_fixture(path):
    with open(path,'r',encoding='utf8') as f:
        return json.load(f)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', help='Path to product JSON', default='data/product_fixture.json')
    p.add_argument('--out_dir', help='Output directory', default='output')
    args = p.parse_args()

    raw = load_fixture(args.input)
    parser = ParserAgent()
    productA = parser.run(raw['product_A'])
    productB = parser.run(raw['product_B'])

    qgen = QuestionGeneratorAgent()
    questions = qgen.run(productA)

    renderer = TemplateRendererAgent()
    faq = renderer.render_faq(productA, questions)
    product_page = renderer.render_product_page(productA)
    comparison = renderer.render_comparison_page(productA, productB)

    exporter = JSONExporterAgent()
    out_dir = args.out_dir
    paths = []
    paths.append(exporter.write(faq, os.path.join(out_dir,'faq.json')))
    paths.append(exporter.write(product_page, os.path.join(out_dir,'product_page.json')))
    paths.append(exporter.write(comparison, os.path.join(out_dir,'comparison_page.json')))

    print('Generated files:')
    for p in paths:
        print(' -', p)
    print('\nOpen the JSON files in the output directory to inspect the results.')

if __name__ == '__main__':
    main()
