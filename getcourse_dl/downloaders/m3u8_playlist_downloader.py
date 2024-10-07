"""
Dload playlist m3u8 file, then dload video.
"""

from getcourse_dl.downloaders.abstract_downloader import AbstractDownloader, DownloaderException
from getcourse_dl.logger.logger import logger, Verbosity
from getcourse_dl.network_wrapper.nwrap import nwrap
import subprocess


class M3U8Downloader(AbstractDownloader):
    def download(self) -> None:
        logger.print(Verbosity.INFO,
                     'Downloading m3u8 link {} target {}'.format(self.url, self.output_path))
        try:
            m3u8_resp = nwrap.get(self.url)
            if m3u8_resp.status_code != 200:
                raise DownloaderException('Can not dload m3u8 playlist')
        except Exception as e:
            raise DownloaderException(
                'Can not dload m3u8 playlist, reason: {}'.format(e))

        if not isinstance(m3u8_resp.content, bytes):
            raise DownloaderException('Content is not bytes')
        with open(self.output_path + '.m3u8', 'wb') as output_file:
            output_file.write(m3u8_resp.content)
        logger.print(
            Verbosity.INFO, 'Downloading {} video via ffmpeg'.format(self.output_path))
        compl_process = subprocess.run(['ffmpeg',
                                        '-protocol_whitelist', 'file,http,https,tcp,tls,crypto',
                                        '-i', self.output_path + '.m3u8',
                                        '-c:v', 'copy',
                                        '-c:a', 'copy',
                                        self.output_path + '.mp4'],
                                       capture_output=True)
        logger.dump(str(compl_process.stdout),
                    self.output_path.replace('/', '_') + '.ffmpeg.stdout')
        logger.dump(str(compl_process.stderr),
                    self.output_path.replace('/', '_') + '.ffmpeg.stderr')
        if compl_process.returncode != 0:
            logger.print(Verbosity.ERROR, 'ffmpeg could not dload playlist. see {}'.format(
                self.output_path + '.ffmpeg.std[out, err]'))
        # ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -i 1080.m3u8  -c:v copy -c:a copy 1080.mp4
