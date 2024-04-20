require("dotenv").config();
const { IgApiClient } = require('instagram-private-api');
const Jimp = require('jimp');
// const fs = require('fs').promises;
const { get } = require('request-promise');
// const CronJob = require("cron").CronJob;
const util = require('util');
// const exec = util.promisify(require('child_process').exec);
const express = require('express')

const app = express()
const port = process.env.PORT || 4000;


app.get('/get-info', async (req, res) => {
    try {
        // Call the get_info function
        fetch('https://flask-heroku-server-3.onrender.com/')
        await get_info();
        res.status(200).send({ message: 'get_info function executed successfully' });
    } catch (error) {
        console.error('Error:', error);
        res.status(500).send({ error: 'An error occurred while executing get_info function' });
    }
});

var imageUrl
var description
var width
var height
var is_valid_return=1
function get_info()
{
    fetch('https://flask-heroku-server-3.onrender.com/post')
    .then(response => {
        return response.json();
    })
    .then(data => {
        console.log(data)
        if (data && data.error === 'Document not found') {
            console.log("yed")
            is_valid_return=-1; // Return -1 if the error indicates document not found
            console.log(is_valid_return)
        }
        else if (data.platform == 1 || data.platform == 4) {
            imageUrl = data.image_url
            description = data.description
            width = data.width
            height = data.height;
            postToInsta();
        }
        else if (data.platform == 3) {
            imageUrl = data.image_url
            description = data.description
            width = data.width
            height = data.height;
            addStoryToInsta();
        }
        else if (data.platform == 5 || data.platform==6) {
            imageUrl = data.image_url
            description = data.description
            width = data.width
            height = data.height;
            post_and_add_story();
        }
    })
    .catch(error => {
    console.error('Error:', error);
    return -1;
    }); 
}

const postToInsta = async () => {
    try {
        const ig = new IgApiClient();
        ig.state.generateDevice(process.env.IG_USERNAME);
        await ig.account.login(process.env.IG_USERNAME, process.env.IG_PASSWORD);
        console.log('Login Successful.');

        const image = await Jimp.read({ url: imageUrl });        

        const overlay = await Jimp.read({url:'https://github.com/Samarth23-sudo/ClubArtizen/blob/main/Club%20Artizen%20Logo%20Circle.png?raw=true'});
        
        if (!image || !overlay) {
            throw new Error('Failed to load images.');
        }
        
        await image.resize(width, height, Jimp.RESIZE_NEAREST_NEIGHBOR).quality(100);

        overlay.resize(width/6.5, width/6.5);

        image.composite(overlay, 10, 10, {
            mode: Jimp.BLEND_SOURCE_OVER,
            opacityDest: 1,
            opacitySource: 1
        });

        await image.writeAsync("result.jpg");

        const resizedImageBuffer = await image.getBufferAsync(Jimp.MIME_JPEG);
        const imageBuffer = resizedImageBuffer;

        await ig.publish.photo({
            file: imageBuffer,
            caption: description,
        });

        console.log('Posted successfully.');
    } catch (error) {
        console.error('Error:', error.message);
    }
};

const addStoryToInsta = async () => {
    try {
        const ig = new IgApiClient();
        ig.state.generateDevice(process.env.IG_USERNAME);
        await ig.account.login(process.env.IG_USERNAME, process.env.IG_PASSWORD);
        console.log('Login Successful.');

        const image = await Jimp.read({ url: imageUrl });

        const overlay = await Jimp.read({url:'https://github.com/Samarth23-sudo/ClubArtizen/blob/main/Club%20Artizen%20Logo%20Circle.png?raw=true'});
        
        if (!image || !overlay) {
            throw new Error('Failed to load images.');
        }
        
        overlay.resize(width/5, width/5);

        image.composite(overlay, 10, 10, {
            mode: Jimp.BLEND_SOURCE_OVER,
            opacityDest: 1,
            opacitySource: 1
        });
        // Resize the image to fit within the 9:16 aspect ratio
        const aspectRatio = width / height;
        const desiredWidth = 1080;
        const desiredHeight = 1920;

        let newWidth, newHeight;
        if (aspectRatio > desiredWidth / desiredHeight) {
            // Fit to width
            newWidth = desiredWidth;
            newHeight = Math.round(newWidth / aspectRatio);
        } else {
            // Fit to height
            newHeight = desiredHeight;
            newWidth = Math.round(newHeight * aspectRatio);
        }

        // Resize the image
        await image.resize(newWidth, newHeight);
        
        
        // Create a new image with the desired aspect ratio and fill it with white color
        const paddedImage = new Jimp(desiredWidth, desiredHeight, 0xFFFFFFFF);

        // Paste the resized image onto the padded image to center it
        const xOffset = Math.floor((desiredWidth - newWidth) / 2);
        const yOffset = Math.floor((desiredHeight - newHeight) / 2);
        paddedImage.composite(image, xOffset, yOffset);

        // Convert the image to buffer
        const imageBuffer = await paddedImage.getBufferAsync(Jimp.MIME_JPEG);

        // Publish the story with the padded image
        await ig.publish.story({
            file: imageBuffer,
            caption: "ClubArtizen",
        });

        console.log('Story Posted successfully.');
    } catch (error) {
        console.error('Error occurred while publishing the story:', error);
    }
};

const post_and_add_story = async () => {
    try {
        const ig = new IgApiClient();
        ig.state.generateDevice(process.env.IG_USERNAME);
        await ig.account.login(process.env.IG_USERNAME, process.env.IG_PASSWORD);

        const image = await Jimp.read({ url: imageUrl });
        console.log('Login Successful.');

        await image.resize(width, height, Jimp.RESIZE_NEAREST_NEIGHBOR).quality(100);

        const overlay = await Jimp.read({url:'https://github.com/Samarth23-sudo/ClubArtizen/blob/main/Club%20Artizen%20Logo%20Circle.png?raw=true'});
        
        if (!image || !overlay) {
            throw new Error('Failed to load images.');
        }
        
        overlay.resize(width/6.5, width/6.5);

        image.composite(overlay, 10, 10, {
            mode: Jimp.BLEND_SOURCE_OVER,
            opacityDest: 1,
            opacitySource: 1
        });

        const resizedImageBuffer = await image.getBufferAsync(Jimp.MIME_JPEG);
        const imageBuffer = resizedImageBuffer;

        await ig.publish.photo({
            file: imageBuffer,
            caption: description,
        });
        console.log('Posted successfully.');

        //Fix the size of the image on story
        // Resize the image to fit within the 9:16 aspect ratio
        const aspectRatio = width / height;
        const desiredWidth = 1080;
        const desiredHeight = 1920;

        let newWidth, newHeight;
        if (aspectRatio > desiredWidth / desiredHeight) {
            // Fit to width
            newWidth = desiredWidth;
            newHeight = Math.round(newWidth / aspectRatio);
        } else {
            // Fit to height
            newHeight = desiredHeight;
            newWidth = Math.round(newHeight * aspectRatio);
        }

        // Resize the image
        await image.resize(newWidth, newHeight);

        // Create a new image with the desired aspect ratio and fill it with white color
        const paddedImage = new Jimp(desiredWidth, desiredHeight, 0xFFFFFFFF);

        // Paste the resized image onto the padded image to center it
        const xOffset = Math.floor((desiredWidth - newWidth) / 2);
        const yOffset = Math.floor((desiredHeight - newHeight) / 2);
        paddedImage.composite(image, xOffset, yOffset);

        // Convert the image to buffer
        const imageBuffer_1 = await paddedImage.getBufferAsync(Jimp.MIME_JPEG);

        // Publish the story with the padded image
        await ig.publish.story({
            file: imageBuffer_1,
            caption: "ClubArtizen",
        });

        console.log('Story Posted successfully.');
    } catch (error) {
        console.error('Error:', error.message);
    }
};

// const cronInsta = new CronJob("18 15 * * *", async () => {
//                                          //post story every day at 9 am
// });

//cronInsta.start();
// get_info();
app.listen(port, () => {
    console.log(`Listening on port ${port}`)
})