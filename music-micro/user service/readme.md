userservice->npm init -y ->npm i -g typescript(global) -> npm i -D typescript (dev dependency to help in aws) -> npm i nodemon concurrently ->npm i express dotenv mongoose bcrypt jsonwebtoken
-> npx tsc -init
->npm i @types/express @types/dotenv @types/mongoose @types/bcrypt @types/jsonwebtoken cors @types/cors
tsc(to build  the typescript  code )
node .\dist\index.js

do some changes in scripts in package.json to run the project.

now do npm run dev
<!-- borium.com -->