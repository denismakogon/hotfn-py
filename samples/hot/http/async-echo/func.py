# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import asyncio

from hotfn.http import response
from hotfn.http import worker


@worker.coerce_input_to_content_type
async def app(context, **kwargs):
    """
    This is just an echo function
    :param context: request context
    :type context: hotfn.http.request.RequestContext
    :param kwargs: contains request body by `data` key,
    in case of coroutine contains event loop by `loop` key
    :type kwargs: dict
    :return: echo of request body
    :rtype: object
    """
    headers = {
        "Content-Type": "plain/text",
    }
    return response.RawResponse(
        context.version, 200, "OK",
        http_headers=headers,
        response_data="OK")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    worker.run(app, loop=loop)
