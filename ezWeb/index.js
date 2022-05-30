const express = require("express");
const { json } = require("express/lib/response");
const { google } = require("googleapis");
const fetch = require('node-fetch');

const app = express();
app.set("view engine", "ejs");
app.use(express.urlencoded({ extended: true }));

app.get("/generateSite", async (req, res) => {

  const { request, name } = req.body;

  const auth = new google.auth.GoogleAuth({
    keyFile: "credentials.json",
    scopes: "https://www.googleapis.com/auth/spreadsheets",
  });

  // Create client instance for auth
  const client = await auth.getClient();

  // Instance of Google Sheets API
  const googleSheets = google.sheets({ version: "v4", auth: client });

  const spreadsheetId = "";

  // Read rows from spreadsheet
  const getRows = await googleSheets.spreadsheets.values.get({
    auth,
    spreadsheetId,
    range: "Sheet1!A:B",
  });

  //extract the url TODO - add the checking of new url here
  console.log(req.query);
  const url = getRows.data.values[req.query.rownumber-1][0];
  const text = getRows.data.values[req.query.rownumber-1][1];
  console.log(`Extracting url and texts... text is ${text} and url is ${url}. -Completed`);
  const tetxtToShow = getRows.data.values[1];

  //get cloudways authentication
  const body = {'email': '0wulike0@gmail.com', 'api_key':''};
  const response = await fetch('https://api.cloudways.com/api/v1/oauth/access_token', {
    method: 'post',
    body: JSON.stringify(body),
    headers: {'Content-Type': 'application/json'}
  });
  const data = await response.json();
  const access_token = data.access_token;
  console.log(`Obtaining cloudwdays authentication... access_token: ${access_token}. -Completed`);
  
  //get the server id
  const serverInfo = await fetch('https://api.cloudways.com/api/v1/server', {
    headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${access_token}`
    }
  });
  const data2 = await serverInfo.json();
  const serverId = (data2.servers)[0].id;
  console.log(`Fetching server information. serverId: ${serverId}. -Completed`);
  
  //add dns record as well as sub-domain on GODADDY (without www)
  await fetch('https://api.godaddy.com/v1/domains/ezwebs.xyz/records', {
    method: 'PATCH',
    headers: {
        'accept': 'application/xml',
        'Content-Type': 'application/json',
        'Authorization': 'sso-key '
    },
    body: JSON.stringify([
        {
            'data': '128.199.142.135', //TODO - change this to dynamically choose server
            'name': `${url}`,
            'port': 80,
            'priority': 10,
            'protocol': 'string',
            'service': 'string',
            'ttl': 600,
            'type': 'A',
            'weight': 10
        }
    ])
  });
  //add dns record as well as sub-domain on GODADDY (with www)
  await fetch('https://api.godaddy.com/v1/domains/ezwebs.xyz/records', {
    method: 'PATCH',
    headers: {
        'accept': 'application/xml',
        'Content-Type': 'application/json',
        'Authorization': 'sso-key '
    },
    body: JSON.stringify([
        {
            'data': '128.199.142.135', //TODO - change this to dynamically choose server
            'name': `www.${url}`,
            'port': 80,
            'priority': 10,
            'protocol': 'string',
            'service': 'string',
            'ttl': 600,
            'type': 'A',
            'weight': 10
        }
    ])
  });
  console.log(`Adding dns record and setting up sub domain. -Completed`); 
  
 //creating new application with the assigned url as label
  await fetch('https://api.cloudways.com/api/v1/app', {
    method: 'POST',
    headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${access_token}`
    },
    body: new URLSearchParams({
        'server_id': '296143',
        'application': 'wordpress',
        'app_label': `${url}`
    })
  });
  console.log(`Creating new applciation with label: ${url}. Please wait.`);
  //await new Promise(resolve => setTimeout(resolve, 240000)); 

  //get the id of the application
  const appLabel = `${url}`; //app label is the url
  //console.log(`applabel is ${appLabel}`);
  let wantedId;
  while(wantedId == undefined) {
    //get the id of the application that we want to update the domain
    const serverInfo = await fetch('https://api.cloudways.com/api/v1/server', {
      headers: {
          'Accept': 'application/json',
          'Authorization': `Bearer ${access_token}`
      }
    });
    const data2 = await serverInfo.json();
    const appIdList = (data2.servers)[0].apps;
    //console.log(appIdList);
    for (const i of appIdList) {
      //console.log(i);
      if (i.label == appLabel) {
        wantedId = i.id;
        console.log('Application created with id ' + `${wantedId} -Completed`);
        break;
      }
    }
    console.log(`Creating application... Please wait.`);
    await new Promise(resolve => setTimeout(resolve, 10000));
  }
  console.log(`Obtaining application information. Application id: ${wantedId}. -Completed`);

  //update the main domain of the application
  await new Promise(resolve => setTimeout(resolve, 120000));
  //console.log(
    await fetch('https://api.cloudways.com/api/v1/app/manage/cname', {
    method: 'POST',
    headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${access_token}`
    },
    body: new URLSearchParams({
        'server_id': `${serverId}`,
        'app_id': `${wantedId}`,
        'cname': `${url}.ezwebs.xyz`
    })
    })
  //);
  console.log(`Updating application CNAME. -Completed`); 

  res.send(getRows.data.values); 

});

app.listen(8080, (req, res) => console.log("running on 8080"));
