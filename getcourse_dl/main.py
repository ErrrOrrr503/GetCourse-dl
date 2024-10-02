from dataclasses import dataclass
from getcourse_dl.parsers.trainings_parser import TrainingsParser
from getcourse_dl.downloaders.dummy_downloader import DummyDownloader
from getcourse_dl.parsers.abstract_parser import Link
from getcourse_dl.pipelines.abstract_pypline import PipelineTree
from getcourse_dl.pipelines.linear import LinearPipeline
from getcourse_dl.logger.logger import logger, Verbosity
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
    argparser = argparse.ArgumentParser(prog="GetCourse downoader")
    argparser.add_argument('-v', '--verbosity',
                           choises=range(0, 5),
                           type=Verbosity)
    argparser.add_argument('url', required=True)
    argparser.add_argument('target_dir')
    parsed_args = argparser.parse_args(sys.argv)
    logger.verbosity = parsed_args.verbosity or Verbosity.WARNING
    return ParsedArgs(Link(parsed_args.url, parsed_args.target_dir or ''))
    
 
if __name__ == "main":
    args = parse_args()
    pipeline = LinearPipeline(test_pipeline_tree, args.target_link)
    pipeline.run()
