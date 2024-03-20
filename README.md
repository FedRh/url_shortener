# URL_shortener

to run the tool use 

docker build -t url_shortener_image --rm .

docker run -it --name url_shortener_app --rm url_shortener

then you will se yourself logged in bash as app_user and you can start run the python commands

to minify a url use

python url_shortener.py --minify="someurl"

to expand 

python url_shortener.py --expand="someurl"

For the sake of semplicity, I didn't manage some things in a proper way:

- the tests would be managed by a CI tool , which run the test before deploying or running the application
- the mongo URI is hardcoded in the docker file as an ENV variable, which is not secure, in a real application I would store the configurations inside a configuration server and retrieve for example a yaml config file from which I would get the data for the db connection
- In the code business logic, I'd also add a URL validation before doing any operation on the urls
- the short code generation would be more secure and efficient, generating and hash with md5 or sha-256 and then getting from the hash the number of charachters desired
