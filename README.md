# To run locally you need to:
* ## Install poetry using the PIP package manager: ***pip install poetry***
* ## Install dependencies: ***poetry install***
* ## Don't forget to select the poetry environment in your development environment!
* * ### Create a file in the project folder: ***.env***
* * ### Add to the file:
  * OPENAI_API_KEY=your_openai_key
  * GITHUB_API_TOKEN=your_github_token
 
# Answer Part 2
As for 100+ new requests for verification per minute, you can organize a request queue, for example, via gather in asyncio.
Or use thread.

Large repositories can be tried to get asynchronously, that is, if we are talking about getting files with a large number of directories, then try to download each directory asynchronously, and at the same time continue to go through the directories

You can also manage the increased number of requests to the OpenAI API by reducing the response token, that is, make the responses shorter using the API settings, and you can also use a cheaper model, gpt 4 turbo is an expensive model, you can currently use gpt 4o mini cheaper
