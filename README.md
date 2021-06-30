<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** github_username, repo_name, twitter_handle, email, project_title, project_description
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/barash/carl_herbie">
    <img src="https://camo.githubusercontent.com/eac13d8c586580b9f6021de514003ba5e6b1734cfef3489d8dfd83006b811d96/68747470733a2f2f61747472616374696f6e736d6167617a696e652e636f6d2f77702d636f6e74656e742f75706c6f6164732f323031392f30332f4865726269652d353074682d616e6e69766572736172792d66656174757265642d363230783331362e6a7067" alt="Logo">
  </a>

<h3 align="center">Carl Herbie</h3>

  <p align="center">
    Herbie System integrated into Carl. Primarily for Marketing projects and
being heavily used for lead generations.
    <br />
    <br />
    <a href="https://github.com/barash/carl_herbie">View Website</a>
    ·
    <a href="https://github.com/barash/carl_herbie/issues">Report Bug</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->

## About The Project

Carl Herbie uses Herbie system to automatically generate endpoints using the power of JSON schema.

### Built With

* [Django](https://www.djangoproject.com/)
* [Python](https://www.python.org/)
* [Herbie](https://github.com/herbie/herbie/)

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* [Python](https://www.python.org/) (For Local Build)
* [Poetry](https://python-poetry.org/) (For Local Build)
* [Docker](https://www.docker.com/) (For Docker Build)
* [Docker Compose](https://docs.docker.com/compose/) (For Docker Build)

### Installation Locally

1. Clone the repo
   ```sh
   git clone https://github.com/barash-asenov/carl_herbie.git
   ```
2. Generate your own .env file
   ```sh
   cp .env.example .env
   ```
3. Create a Database and Update .env credentials and update the
   `DATABASE_URL` on .env file.
4. Hook Into Virtual Environment
   ```sh
    poetry shell
    ```
5. Install Poetry packages
   ```sh
   poetry install
   ```
6. Generate Model Classes
   ```sh
   python manage.py generatemodels
   ```
7. Generate and Run the Migrations
   ```sh
   python manage.py makemigrations
   python manage.py migrate 
   ```
8. Load Schemas into Database
   ```sh   
   python manage.py import_json_schemas
   ```
9. Create SuperUser in the admin dashboard
   ```sh
   python manage.py createsuperuser --username "username" --email "email@email-address.com"
   ```

### Installation through Docker

To be filled