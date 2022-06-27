const express = require("express");
const { json } = require("express/lib/response");
const { google } = require("googleapis");
const fetch = require('node-fetch');
console.log(process.cwd());
const app = express();
app.set("view engine", "ejs");
app.use(express.urlencoded({ extended: true }));
const request = require('request');
const fs = require("fs");
let path = require("path");
const fsExtra = require('fs-extra')





/*---------------------------------------POST MANIPULATION----------------------------------------*/


//create post
/*
  the request body must contain both the post and the url of the website to be updated.
*/
app.use(express.json());
app.post("/createPost", async (req, res) => {
  const response = await fetch(`https://${req.body.websiteName}.ezwebs.xyz/wp-json/wp/v2/posts`);
  const responseObject = await response.json();
  let duplicate = false;
  console.log(responseObject);
  for (let i in responseObject) {
    console.log(responseObject[i]);
    //console.log(i.title.rendered);
    if (responseObject[i].title.rendered == req.body.title) {
      duplicate = true;
    }
  }
  if (duplicate) {
    console.log(`duplicate found`);
    res.sendStatus(404); //if the same title already exists, do nothing and return 404 error code
  } else {
    const createdPost = 
    await fetch(`https://${req.body.websiteName}.ezwebs.xyz/wp-json/wp/v2/posts`, {
      //await fetch(`https://witnessmagic.com.ezwebs.xyz/wp-json/wp/v2/posts`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Basic ${Buffer.from("0wulike0@gmail.com:oTK5 KTLF U8lG EfpT C5vn qzlG", "utf-8").toString("base64")}`
      },
      body: JSON.stringify({
        title : req.body.title,
        content: req.body.content,
        status: "publish"
      })
    });
    const postBody = await createdPost.json();
    console.log(postBody);
    const id = postBody.id;
    console.log("id is" + id);
    /* console.log(await createdPost.text());
    const response = await fetch(`https://witnessmagic.com.ezwebs.xyz/wp-json/wp/v2/posts?per_page=1`);
    console.log(await response.text());
    res.send();
    console.log('post created'); */
    res.send(`${id}`); //send the id back to the ezweb google sheet database
  }
});

//amend post
/*
  the request body must contain both the post, post id and the url of the website to be updated.
*/

app.post("/updatePost", async (req, res) => {
  console.log(req.body);
  console.log(await fetch(`https://${req.body.websiteName}.ezwebs.xyz/wp-json/wp/v2/posts/${req.body.postId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Basic ${Buffer.from("0wulike0@gmail.com:oTK5 KTLF U8lG EfpT C5vn qzlG", "utf-8").toString("base64")}`
    },
    body: JSON.stringify({
      title : req.body.title,
      content: req.body.content,
    })
  }));
  res.send();
});

//delete post
/*
  the request body must contain both the post, post id and the url of the website to be updated.
*/
app.post("/deletePost", async (req, res) => {
  console.log(await fetch(`https://${req.body.websiteName}.ezwebs.xyz/wp-json/wp/v2/posts/${req.body.postId}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Basic ${Buffer.from("0wulike0@gmail.com:oTK5 KTLF U8lG EfpT C5vn qzlG", "utf-8").toString("base64")}`
    }
  }));
  console.log(req.body);
  res.send();
});

//retrieve the latest post
/*
  the request body must contain both the post, spost id and the url of the website to be updated.
*/
app.get("/retrievePost", async (req, res) => {
  const response = await fetch(`https://${req.body.websiteName}.ezwebs.xyz/wp-json/wp/v2/posts`);
  const jsonObject = await response.json();
  console.log(jsonObject);
  const result = {};
  for (let i in jsonObject) {
    jsonObject[i].content = jsonObject[i].content.rendered;
    jsonObject[i].title = jsonObject[i].title.rendered;
    //result[jsonObject[i].title.rendered] = jsonObject[i].id;
  }
  console.log(result);
  res.send(JSON.stringify(jsonObject));
  }
);


/*---------------------------------------POST MANIPULATION----------------------------------------*/



/*---------------------------------------LISTING MANIPULATION----------------------------------------*/


//create post
/*
  the request body must contain both the post and the url of the website to be updated.
*/
app.use(express.json());


app.post("/uploadImage", async (req, res) => {
  const fs = require('fs');
  let path = require("path");
  const contents = fs.readFileSync(path.resolve(__dirname, "1.png"));
  //console.log(contents);
  const response = await fetch('https://${req.body.websiteName}.ezwebs.xyz/wp-json/wp/v2/media', {
    method: 'POST',
    headers: {
        'cache-control': 'no-cache',
        'content-type': 'image/png',
        'content-disposition' : `attachment; filename="1.png"`,
        "Accept": "application/json",
        'authorization': `Basic ${Buffer.from("0wulike0@gmail.com:oTK5 KTLF U8lG EfpT C5vn qzlG", "utf-8").toString("base64")}`,
    },
    body: contents
  });
  const error = await response.json();
  console.log(error);
  res.send(response);
})


app.post("/createListing", async (req, res) => {

  const response = await fetch(`https://${req.body.websiteName}.ezwebs.xyz/wp-json/wp/v2/listing`);
  const responseObject = await response.json();
  let duplicate = false;
  for (let i in responseObject) {
    if (responseObject[i].title.rendered == req.body.title) {
      duplicate = true;
    }
  }
  if (duplicate) {
    console.log(`duplicate found`);
    res.sendStatus(404); //if the same title already exists, do nothing and return 404 error code
  } else {

  
    //download the featured pciture to local environment
    //download the featured pciture to local environment
    const downloadFile = new Promise(async resolve => {
      const imageSteram = await (request.get(`${req.body.featured_photo_file_path}`)
      .on('error',function(err){
      console.log(err);
      })
      .on('response',function(response){
      if(response.statusCode == 200){
      console.log("successfully retreived image from url");
      }
      }));
      const b = fs.createWriteStream('pictures/' + `${req.body.featured_photo_file_id}.jpg`);
      imageSteram.pipe(b); 
      b.on('finish', resolve);
    });
    await downloadFile;

    //upload the featured image to the site
    const contents = fs.readFileSync(path.resolve(__dirname, `pictures/${req.body.featured_photo_file_id}.jpg`));
    console.log(contents);
    console.log(req.body);
    const response = await fetch(`https://${req.body.websiteName}.ezwebs.xyz/wp-json/wp/v2/media`, {
    method: 'POST',
    headers: {
        'cache-control': 'no-cache',
        'content-type': 'image/jpg',
        'content-disposition' : `attachment; filename="${req.body.featured_photo_file_id}.jpg"`,
        "Accept": "application/json",
        'authorization': `Basic ${Buffer.from("0wulike0@gmail.com:oTK5 KTLF U8lG EfpT C5vn qzlG", "utf-8").toString("base64")}`,
    },
    body: contents
    });
    const responseBody = await response.json();

    const featuredImageId = responseBody.id;
    //cler the local picture database.
    //fsExtra.emptyDirSync('./pictures');
 
    const idArrayExtra = [];
    const extraPhotos = req.body['extra_photos'];
    console.log(extraPhotos);
    //download the extra_photos to local
    for (const i of extraPhotos) {
      let extraP = i['file_path'];
      let extraId = i['file_id'];
      const downloadFile = new Promise(async resolve => {
        const imageStream2 = await (request.get(`${extraP}`)
        .on('error',function(err){
        console.log(err);
        })
        .on('response',function(response){
        if(response.statusCode == 200){
        console.log("successfully retreived image from url");
        }
        }));
        const a = fs.createWriteStream('pictures/' + `${extraId}.jpg`);
        imageStream2.pipe(a); 
        a.on('finish', resolve);
      });
      await downloadFile;


      //upload the extra_photos to wordpress
      const contents2 = fs.readFileSync(path.resolve(__dirname, `pictures/${extraId}.jpg`));
      console.log(contents2);
      const response2 = await fetch(`https://${req.body.websiteName}.ezwebs.xyz/wp-json/wp/v2/media`, {
      method: 'POST',
      headers: {
          'cache-control': 'no-cache',
          'content-type': 'image/jpg',
          'content-disposition' : `attachment; filename="${extraId}.jpg"`,
          "Accept": "application/json",
          'authorization': `Basic ${Buffer.from("0wulike0@gmail.com:oTK5 KTLF U8lG EfpT C5vn qzlG", "utf-8").toString("base64")}`,
      },
      body: contents2
      });
      const responseBody2 = await response2.json();
      const extraImageId = responseBody2.id;
      idArrayExtra.push(extraImageId)
    } 
    //clear the local picture database
    fsExtra.emptyDirSync('./pictures');
    console.log('id array is' + idArrayExtra); 
   
    //create the listing with given information
    console.log(featuredImageId);
    const createdPost = await fetch(`https://${req.body.websiteName}.ezwebs.xyz/wp-json/wp/v2/listing`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Basic ${Buffer.from("0wulike0@gmail.com:oTK5 KTLF U8lG EfpT C5vn qzlG", "utf-8").toString("base64")}`
      },
      body: JSON.stringify (
        {
          title : req.body.title,
          content: req.body.description,
          price: req.body.price,
          property_type: req.body.property_type,
          number_of_rooms: req.body.num_rooms,
          total_area: req.body.total_area,
          year_built: req.body.year_built,
          level: req.body.number_of_storeys,
          address: req.body.address,
          status: "publish",
          tenure: req.body.tenure,
          featured_media: featuredImageId,
          gallery: idArrayExtra
        }
      )

    });
    const postBody = await createdPost.json();
    console.log(postBody);
    const id = postBody.id;
    //console.log("id is" + id);
    /* console.log(await createdPost.text());
    const response = await fetch(`https://witnessmagic.com.ezwebs.xyz/wp-json/wp/v2/posts?per_page=1`);
    console.log(await response.text());
    res.send();
    console.log('post created'); */
    res.send(`${id}`); //send the id back to the ezweb google sheet database
  }
});

app.post("/deleteListing", async (req, res) => {
  console.log(await fetch(`https://${req.body.websiteName}.ezwebs.xyz/wp-json/wp/v2/listing/${req.body.postId}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Basic ${Buffer.from("0wulike0@gmail.com:oTK5 KTLF U8lG EfpT C5vn qzlG", "utf-8").toString("base64")}`
    }
  }));
  console.log(req.body);
  res.send();
});

//retrieve the latest post
/*
  the request body must contain both the post, post id and the url of the website to be updated.
*/
app.get("/retrieveListing", async (req, res) => {
  const response = await fetch(`https://${req.body.websiteName}.ezwebs.xyz/wp-json/wp/v2/listing`);
  const jsonObject = await response.json();
  const result = {};
  for (let i in jsonObject) {
    result[jsonObject[i].title.rendered] = jsonObject[i].id;
  }
  console.log(result);
  res.send(jsonObject);
  }
);
/*---------------------------------------LISTING MANIPULATION----------------------------------------*/


app.get("/retrieveSiteSetting", async (req, res) => {
  const response = await fetch(`https://wefawoeifjawoeijfaweif.com.ezwebs.xyz/wp-json/my-custom-route/v1/Opt?option_name=siteSettingEndpoint_agentpicture2`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Basic ${Buffer.from("0wulike0@gmail.com:oTK5 KTLF U8lG EfpT C5vn qzlG", "utf-8").toString("base64")}`
    }
  });
  const jsonObject = await response.json();
  console.log(jsonObject);
  res.send(jsonObject);
  }
);

app.post("/updateSiteSetting", async (req, res) => {
  
    //download the featured pciture to local environment
    //download the featured pciture to local environment
    const downloadFile1 = new Promise(async resolve => {
      console.log(req.body);
      console.log(req.body.agentpicture1);
      const imageSteram1 = await (request.get(`${(req.body.agentPicture)[0].file_path}`)
      .on('error',function(err){
      console.log(err);
      })
      .on('response',function(response){
      if(response.statusCode == 200){
      console.log("successfully retreived image from url");
      }
      }));
      const b = fs.createWriteStream('pictures/' + `${(req.body.agentPicture)[0].file_id}.jpg`);
      imageSteram1.pipe(b); 
      b.on('finish', resolve);
    });
    await downloadFile1;

    //upload the featured image to the site
    const contents1 = fs.readFileSync(path.resolve(__dirname, `pictures/${(req.body.agentPicture)[0].file_id}.jpg`));
    console.log(contents1);
    console.log(req.body);
    const response1 = await fetch(`https://${req.body.websiteName}.ezwebs.xyz/wp-json/wp/v2/media`, {
    method: 'POST',
    headers: {
        'cache-control': 'no-cache',
        'content-type': 'image/jpg',
        'content-disposition' : `attachment; filename="${(req.body.agentPicture)[0].file_id}.jpg"`,
        "Accept": "application/json",
        'authorization': `Basic ${Buffer.from("0wulike0@gmail.com:oTK5 KTLF U8lG EfpT C5vn qzlG", "utf-8").toString("base64")}`,
    },
    body: contents1
    });
    const responseBody1 = await response1.json();

    const featuredImageId1 = responseBody1.id;


    //download the featured pciture to local environment
    const downloadFile2 = new Promise(async resolve => {
      const imageSteram2 = await (request.get(`${(req.body.agentPicture)[1].file_path}`)
      .on('error',function(err){
      console.log(err);
      })
      .on('response',function(response){
      if(response.statusCode == 200){
      console.log("successfully retreived image from url");
      }
      }));
      const b = fs.createWriteStream('pictures/' + `${(req.body.agentPicture)[1].file_id}.jpg`);
      imageSteram2.pipe(b); 
      b.on('finish', resolve);
    });
    await downloadFile2;

    //upload the featured image to the site
    const contents2 = fs.readFileSync(path.resolve(__dirname, `pictures/${(req.body.agentPicture)[1].file_id}.jpg`));
    console.log(contents2);
    console.log(req.body);
    const response2 = await fetch(`https://${req.body.websiteName}.ezwebs.xyz/wp-json/wp/v2/media`, {
    method: 'POST',
    headers: {
        'cache-control': 'no-cache',
        'content-type': 'image/jpg',
        'content-disposition' : `attachment; filename="${(req.body.agentPicture)[1].file_id}.jpg"`,
        "Accept": "application/json",
        'authorization': `Basic ${Buffer.from("0wulike0@gmail.com:oTK5 KTLF U8lG EfpT C5vn qzlG", "utf-8").toString("base64")}`,
    },
    body: contents2
    });
    const responseBody2 = await response2.json();

    const featuredImageId2 = responseBody2.id;
    console.log('id is' + featuredImageId1);
    //clear the local picture database
    fsExtra.emptyDirSync('./pictures');
    const featuredImageId1array = [];
    featuredImageId1array.push(featuredImageId1);
    const featuredImageId2array = [];
    featuredImageId2array.push(featuredImageId2);

    await new Promise(resolve => setTimeout(resolve, 20000));

  const response = await fetch(`https://${req.body.websiteName}.ezwebs.xyz/wp-json/my-custom-route/v1/updateOpt/`, {
    //https://wordpress-296143-2675827.cloudwaysapps.com/wp-json/wp/v2/settings
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Basic ${Buffer.from("0wulike0@gmail.com:oTK5 KTLF U8lG EfpT C5vn qzlG", "utf-8").toString("base64")}`

    },
      body: JSON.stringify (
        {
          //title : req.body.title,
          siteSettingEndpoint_agentpicture1: featuredImageId1array,
          'siteSettingEndpoint_agentpicture2': featuredImageId2array,
          'siteSettingEndpoint_agentnumber': req.body.agentNumber,
          'siteSettingEndpoint_agentname': req.body.agentName,
          'siteSettingEndpoint_agentemail': req.body.agentEmail,
          'siteSettingEndpoint_agentquote': req.body.agentQuote,
          'siteSettingEndpoint_aboutme': req.body.aboutMe
        }
      )
    });
  //const jsonObject = await response.json();
  console.log(response);
  res.send(response);
  }
);





/*---------------------------------------SITE GENERATION----------------------------------------*/
//endpoint for bot to call to check availability and price
app.get("/checkURL", async (req, res) => {
  const domainInfo = await fetch(`https://api.godaddy.com/v1/domains/available?domain=${req.query.urlToCheck.slice(4)}&checkType=full&forTransfer=false`, {
      headers: {
          'accept': 'application/json',
          'Authorization': 'sso-key e4XjqrBbV2A9_FRhBpvFQXPJCyYo5HZx7eb:T6C4GjmVF6XAihr1Kx5vif'
      }
  });
  console.log(domainInfo)
  const jsonDomainInfo = await domainInfo.json();
  console.log(jsonDomainInfo);
  if (jsonDomainInfo.price == undefined) {
    res.send(JSON.stringify({ availability: jsonDomainInfo.available, price: 0}));
  } else {
    res.send(JSON.stringify({ availability: jsonDomainInfo.available, price: jsonDomainInfo.price/1000000}));
  }
});

//Generate a new website
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

  const spreadsheetId = "1ipRmmou_iSL_tkpuvppXiA7XQz3Nby_9XRF6zEaQoqI";

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
  const body = {'email': '0wulike0@gmail.com', 'api_key':'3I0UOYFiNd9zH11sTymV3W9UjYWMMm'};
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
        'Authorization': 'sso-key e4XjqrBbV2A9_P5WmWpBEYGckGWDZwwpu8P:UUCGcrUhZZ39VbEAtNF4eq'
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
        'Authorization': 'sso-key e4XjqrBbV2A9_P5WmWpBEYGckGWDZwwpu8P:UUCGcrUhZZ39VbEAtNF4eq'
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
  
  //Creating new application with assigned url as label, by cloning
  fetch('https://api.cloudways.com/api/v1/app/clone', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${access_token}`,
        'Accept': 'application/json'
    },
    body: new URLSearchParams({
        'server_id': `${serverId}`,
        'app_id': '2675827', //thi is the snapshotted application
        //https://wordpress-296143-2675827.cloudwaysapps.com/
        'app_label': `${url}`
    })
  });
  console.log(`Creating new applciation with label: ${url}. Please wait.`);

 /* //creating new application with the assigned url as label
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
  console.log(`Creating new applciation with label: ${url}. Please wait.`); */
  //await new Promise(resolve => setTimeout(resolve, 240000));  */

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
  await new Promise(resolve => setTimeout(resolve, 240000)); //wait for 4 minutes for the application to be created
  //console.log(
    console.log(await fetch('https://api.cloudways.com/api/v1/app/manage/cname', {
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
    }));
  //);
  console.log(`Updating application CNAME. -Completed`); 
  await new Promise(resolve => setTimeout(resolve, 180000)); //wait for 3 minutes for the CNAME to be updated
  //set up SSL certificate
  console.log(await fetch('https://api.cloudways.com/api/v1/security/lets_encrypt_install', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'Authorization': `Bearer ${access_token}`
    },
    body: `server_id=${serverId}&app_id=${wantedId}&ssl_email=websitegurusingapore%40gmail.com&wild_card=false&ssl_domains[]=www.${url}.ezwebs.xyz&ssl_domains[]=${url}.ezwebs.xyz`
  }));

  //application password - 0wulike0@gmail.com:cTU6 RfVa 90H9 fCma mK6Q ET42
  await new Promise(resolve => setTimeout(resolve, 180000)); //wait for 3 minutes for SSL to be set up. 
  //updating the created site's title to be the input text
  console.log(await fetch(`https://${url}.ezwebs.xyz/wp-json/wp/v2/settings`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Basic ${Buffer.from("0wulike0@gmail.com:oTK5 KTLF U8lG EfpT C5vn qzlG", "utf-8").toString("base64")}`
    },
    body: JSON.stringify({
      title: `${text}`,
    })
  }));



  res.send(getRows.data.values); 

});




app.listen(8080, (req, res) => console.log("running on 8080"));
