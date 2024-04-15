---
date: 2024-04-15T13:07:15.652688
author: AutoGPT <info@agpt.co>
---

# watermark-test

The task involves creating a solution that allows users to add text or image watermarks to PDF files. This solution must offer flexibility and control over the watermark's customization, including its opacity, position, and size, ensuring that the watermark does not obscure the content of the PDF. From the user's perspective, both text and image watermarks are essential for different use cases, with text watermarks being favored for their simplicity in certain contexts, and image watermarks being critical for branding purposes.

The envisioned interface for this solution includes a web-based platform where users can upload the PDF and the watermark file (whether text or image) through a user-friendly mechanism such as a drag-and-drop area or a file upload button. The platform should support popular image formats for image watermarks and provide clear labeling of each upload section to avoid user confusion. To adjust the watermark settings, a side panel or modal window should allow users to modify parameters like opacity, position, scale, and rotation. A real-time preview feature is also highly desired for users to see the watermark's appearance on the PDF before the finalizing step.

For the implementation, using Python is recommended due to its robust libraries for PDF manipulation such as PyPDF2 and ReportLab. These libraries can handle the technical requirements needed for implementing the watermarking functionality effectively, including adjusting the opacity of elements, preserving the original document's quality, and ensuring compatibility across various PDF viewers. Best practices include using transparent overlays to maintain document usability, securing the watermarks against removal, and optimizing the performance for batch processing scenarios.

This solution requires careful consideration of copyright and privacy laws to ensure the practice of watermarking complies with legal standards. Finally, providing detailed customization options allows the tool to cater to a broad range of needs, from simple copyright assertion to complex branding strategies.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'watermark-test'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
