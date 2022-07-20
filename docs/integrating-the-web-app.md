---
layout: page
title:  "Web App Hosting and Integration into a Partner's Website"
---

The Energy Policy Simulator (EPS) web application is a program that runs on a webserver and allows users to [interact with the model using a web browser](online-model-tutorial.html).  The EPS model itself is free and open-source (per its [software license](software-license.html)) and can be [downloaded](download.html) and run locally on your Windows PC or Mac.  In contrast, the web interface consists of proprietary server-side code owned by Energy Innovation LLC.

### Web Application Hosting

Though the EPS web application may appear small and self-contained, it is in actuality a complicated set of programs running on a server, relying on various server-side technologies, such as a multi-context Vensim library, nginx web server, Ubuntu linux, Ruby, Rails, Passenger, a SQL database, downtime monitoring, security, backups, and more.  An automated build system developed in-house at Energy Innovation allows for rapid prototyping and deployment of new or updated EPS models to staging servers for validation before pushing them to production servers.  The web application interfaces work together with this build system as a tightly-integrated whole.  Some of the steps and tools are configured specifically for Amazon Web Services, the webhost used by EPS, and will not work on other hosting platforms.

Energy Innovation has worked with many partners around the world to produce versions of the EPS for various geographies.  (These EPS versions can be accessed from the [global EPS homepage](https://www.energypolicy.solutions).)  Energy Innovation has invested years of effort in developing the web interface and associated server-side infrastructure to provide partners with a way to deploy their customized EPS models online in a beautiful and highly functional web interface while requiring very little effort and no software engineering knowledge.  Energy Innovation will deploy a partner's EPS model in a web interface free of charge.

Moreover, Energy Innovation handles ongoing hosting costs for EPS web applications and routinely delivers crucial security updates, bug fixes, and user interface improvements to the web application itself and its underlying infrastructure components.  Thus, even if a particular region's EPS model has not been updated for a long time, the web interface running that model is likely much newer.  All EPS servers are maintained and updated on an ongoing basis by Energy Innovation.  Keeping them on a unified software platform under the same Amazon Web Services account is necessary to ensure so many EPS models can be maintained without excessive IT complexity and without falling behind on security updates for any server.

Additionally, because the build system must be able to stage and build EPS models from any EPS region (including regions currently in-development and not yet publicly released, as well as one or two regions where data are governed by a confidentiality agreement with a partner organization), the web application automated build system has access to non-public data.

Partner organizations occasionally ask if they can self-host the EPS web interface.  **This is not possible.**  Due to the complexity of the EPS web application infrastructure, the cross-regional functionality of the automated build system, the need for all web apps to be on the latest software platform for maintainability and security, and the need to ensure non-public data from one partner are not disclosed to any other partner, Energy Innovation cannot share any of the web interface's software code nor permit partners to self-host a copy of the web interface.

Most partners who ask about self-hosting the EPS web interface are simply looking for a way to integrate the EPS into their own, preexisting websites.  Fortunately, this integration can be done seamlessly without any need for the partner to host the web interface.

### Supported Procedure for Integration into Partner Websites

If your organization is working with Energy Innovation to put your EPS model online using the web interface, you are under no obligation to integrate it into your own website.  All EPS web apps are given a unique subdomain of the `energypolicy.solutions` domain (e.g. `poland`, `virginia`, `canada`, etc.), and your EPS model will be accessible there.  Most of our partners have found this to be sufficient.  However, if you do wish to integrate the EPS into your organization's website, this can be done using the following procedure:

1. Choose a subdomain name you want for the simulator.  In a URL, a subdomain follows the `https://` and precedes the domain name and extension.  For example, if your organization's website is at `www.partnerorganization.org` and you select the subdomain `eps` for your model, the simulator will be reached at `eps.partnerorganization.org`.

2. Once your EPS model is running in the web interface on a production server, Energy Innovation will inform you of that server's IP address.  Access your DNS (Domain Name System) management interface.  (The DNS manager is usually either the company you use as your domain name registrar or the company you use to host your website.)  Add an `A record` to your DNS using your chosen subdomain name pointing at the IP address for your production server.

3. Optionally, if you want the simulator to be accessible at a subdirectory URL (such as `www.partnerorganization.org/eps`), you may add a redirect to your site that sends visitors from the subdirectory to the subdomain URL.

4. Incorporate links to the simulator at its new URL to your existing website.  Here, "links" does not just mean hypertext links in the body content of your webpages - "links" can also be in your sites' existing navigation menus and can look like links to any other page on your site.

This procedure allows the EPS web interface to appear to be an integrated part of your website without requiring you to physically host the web application on your servers.  Steps 1-3 can be done before the new simulator is made available to the public.

For consistency in naming, the simulator will *also* remain accessible at its URL on the `energypolicy.solutions` domain.

### Examples

The following partners have chosen to use the supported method above to integrate the EPS with their websites.  Their EPS models can be accessed at the following URLs on their domains:

* [https://eps.kapsarc.org/](eps.kapsarc.org) - King Abdullah Petroleum Studies and Research Center, Saudi Arabia
* [https://policysolutions.pembina.org/](policysolutions.pembina.org) - Pembina Institute, Canada
