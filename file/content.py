from security import *
from http.meta import HTTP, TAGS
from conf.basic import *


def gen_file_location(base_dir, url):
    last_index = len(base_dir) - 1

    # match last character in base directory as '/' , if so - clear it
    if base_dir[last_index:] is TAGS.URL_ROOT:
        base_dir = base_dir[:last_index]

    # match first character in url as '/', if so - clear it
    if url[0:1] is TAGS.URL_ROOT:
        url = url[1:]

    # return with '/' inserted middle - safe mode
    return "".join([base_dir, TAGS.URL_ROOT, url])


class ContentManager:
    def __init__(self, url=DEFAULT_FILE, document_root=DOCUMENT_ROOT):
        self.document_root = document_root
        self.url = url
        # file location will be set during path validation
        self.file_location = None

    def read(self):
        # need to send primary status in response
        primary_status, content = self.read_file()

        # todo - implementation with 304
        # if content is None means error state
        if content is None:
            content = self.handle_content_failure(primary_status)

        return primary_status, content

    def read_file(self):
        # set http status based on directory/file existence, access-permission, reading
        status = self.validate_path()

        # only read if file available with readable (exists, access, read)
        content = None
        if status is HTTP.OK:
            content = open(self.file_location, 'r').read()

        return status, content

    def validate_path(self):

        # bad bots may try to access parent folder of document root - security issue.
        if is_backward_access(self.url):
            return HTTP.BAD_REQUEST

        # document root should be exists, a directory , with access permissions
        if not exists(self.document_root) or not isdir(self.document_root) or not is_accessible(self.document_root):
            return HTTP.SERVER_ERROR

        # matches '/' request path & set into 'index.html'
        if self.url is TAGS.URL_ROOT:
            self.url = DEFAULT_FILE

        # join both document root & request path
        self.file_location = gen_file_location(self.document_root, self.url)

        # if file exists, check below criteria
        if exists(self.file_location):

            #  if joined path is again a directory, join with 'index.html'
            if isdir(self.file_location):
                self.file_location = gen_file_location(self.file_location, DEFAULT_FILE)
                # any how, now it should be file for both file & directory request - if does not match means 'Not Found'
                if not exists(self.file_location):
                    # print "Not found: ", self.file_location
                    return HTTP.NOT_FOUND

            # file readability ensures we can progress through
            if is_readable(self.file_location):
                return HTTP.OK
        else:
            # means file not exists
            # print "Not found: ", self.file_location
            return HTTP.NOT_FOUND

        return HTTP.SERVER_ERROR

    def handle_content_failure(self, primary_status):

        # choose file as per http status
        if primary_status is HTTP.BAD_REQUEST:
            self.url = BAD_REQ_FILE

        elif primary_status is HTTP.NOT_FOUND:
            self.url = NOT_FOUND_FILE

        elif primary_status is HTTP.SERVER_ERROR:
            self.url = SERVER_ERROR_FILE

        # status is useless, we use primary status
        status, content = self.read_file()

        # in case of non-existence, default error msg set
        if content is None:
            content = INTERNAL_ERROR

        # only content returned
        return content
