# Car Images

This folder is for storing car images to display in your dashboard.

## Adding Your Car Image

### Option 1: Use Your Own Photo
1. Take a photo of your Tesla
2. Save it as `my_tesla.jpg` or `my_tesla.png`
3. Place it in this `images` folder
4. Update your dashboard YAML to reference: `/local/community/teslamate/images/my_tesla.jpg`

### Option 2: Download Official Tesla Images

**Model Y Performance:**
- Visit: https://www.tesla.com/modely
- Right-click on the Model Y image → Save Image As
- Save to this folder

**Model 3:**
- Visit: https://www.tesla.com/model3
- Save desired image to this folder

**Model S:**
- Visit: https://www.tesla.com/models
- Save desired image to this folder

**Model X:**
- Visit: https://www.tesla.com/modelx
- Save desired image to this folder

### Option 3: Use Stock Images
Search for "Tesla Model Y Performance" on free stock photo sites:
- Unsplash: https://unsplash.com/s/photos/tesla-model-y
- Pexels: https://www.pexels.com/search/tesla/
- Pixabay: https://pixabay.com/images/search/tesla/

Download and save to this folder.

## Using the Image in Your Dashboard

After adding your image, update the picture entity card in your dashboard:

```yaml
type: picture-entity
entity: device_tracker.tesla_location
image: /local/community/teslamate/images/my_tesla.jpg
show_state: false
show_name: false
```

**Note:** The path `/local/community/teslamate/images/` assumes you installed via HACS. If you installed manually, adjust the path accordingly.

## Recommended Image Specs
- **Format:** JPG or PNG
- **Size:** 1920x1080 or 1280x720 (landscape orientation)
- **File size:** Under 500KB for fast loading
- **Content:** Clear side or 3/4 view of the vehicle
