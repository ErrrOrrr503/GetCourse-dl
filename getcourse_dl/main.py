from dataclasses import dataclass
from getcourse_dl.parsers.trainings_parser import TrainingsParser
from getcourse_dl.downloaders.dummy_downloader import DummyDownloader
from getcourse_dl.parsers.abstract_parser import Link
from getcourse_dl.pipelines.abstract_pypline import PipelineTree
from getcourse_dl.pipelines.linear import LinearPipeline
from getcourse_dl.logger.logger import logger, Verbosity
from getcourse_dl.network_wrapper.nwrap import nwrap
import argparse
import sys

test_pipeline_tree = PipelineTree(TrainingsParser)
test_pipeline_tree.append_child(DummyDownloader)
#todo: append_child returns child to allow further append
#and in general gentle pipeline specification. It's mental illness now.


@dataclass
class ParsedArgs:
    target_link: Link


def parse_args() -> ParsedArgs:
    """ perform all args verification and print usage """
    argparser = argparse.ArgumentParser(prog="GetCourse downoader")
    argparser.add_argument('-v', '--verbosity',
                           choices=range(0, 6),
                           type=int,
                           help='Verbosity')
    argparser.add_argument('-o', '--output_target_dir', help='Where to store failes')
    argparser.add_argument('-u', '--url', help='Link to the cource', required=True)
    argparser.add_argument('-b', '--browser', help='Browser, to load cookies from')
    parsed_args = argparser.parse_args(sys.argv[1:])
    logger.verbosity = Verbosity.WARNING
    try:
        logger.verbosity = Verbosity(int(parsed_args.verbosity))
    except TypeError:
        pass  # ignore
    nwrap.load_cookies(parsed_args.browser)
    logger.print(Verbosity.INFO, 'url={}'.format(parsed_args.url))
    #if len(parsed_args.url) == 0:
    #    argparser.print_help()
    return ParsedArgs(Link(parsed_args.url, parsed_args.output_target_dir or ''))

 
if __name__ == "__main__":
    args = parse_args()
    pipeline = LinearPipeline(test_pipeline_tree, args.target_link)
    pipeline.run()
