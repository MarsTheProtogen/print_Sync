# ✨ About This Project

## 🎭 Who Am I?

I am a technology-driven problem solver currently studying electrical or mechanical engineering. My alias is marstheprotogen online, but my actual name is Landon. My interests lie at the intersection of automation, programming, and hands-on engineering, with a strong foundation in 3D printing, software development, and system design. I also dabble in art from 3d to pencin drawings.

My experience includes:

3D Modeling & Printing → Working with CAD and physical mesurements to develop functional and mechanical parts.

Programming & Automation → Developing tools and software for me to do less.

Hardware & Engineering Applications → Applying knowledge of electronics, mechanics, and fabrication to solve problems.

This is my first speedrun of a development project and it went better than i expected, considering tha personal projects tend to get pushed back a lot.

## 🎯 Why I Created This Project

This project began as a **personal challenge** to address a problem I encountered with file submissions for 3D printing. The objective was to create a system that could:

- **Automate file reception**

- **Scan for potential security risks**

- **Estimate printing costs instantly**


By doing so, pricing information could be sent at any time of the day, eliminating the need for constant manual intervention.

Although initially set as a three-day challenge, the project is still evolving as I refine and expand its capabilities.

---

## the breakdown
When I first started the project I had an idea of what needed to be done and broke it into three parts 
- **inter-server comunucation**

    Being able to have two devices check on eachother's statuses withouut downloading anything to prevent cross contamination
- *8file scaning**

    Finding methods or libraries to check the integrity of files
- **automating**

    Connecting together all the parts and to interact with services used like gmail and google drive


---

## 🚧 Challenges

Throughout development, I encountered several hurdles, including:

🔹 **Tight Deadlines & New Libraries** - Adapting to new libraries or having to swich within a strict timeframe was challenging.

🔹 **Workflow Integration Issues** - Merging multiple functions and files into a cohesive program.

🔹 **Balancing Speed & Functionality** - The time alloted between protptype and implementation cause a lot of unoptimizations and messes.


---

## 🔍 Specific Use Case

This system was designed primarily for personal use, providing a way to:

📂 **Receive 3D print files automatically**
💰 **Estimate printing costs instantly**
⏳ **Allow fast response times without manual oversight**
🔶 **scn files for possible DoS errors**

It ensures that files are received, processed, and priced efficiently—making the system highly accessible **at any time of the day**, while keeping compuuter software safe. 

---

## 🎉 Best Part of the Project

One of the most exciting parts of this project was **creating lightweight techniques** to:

✔️ **Differentiate 3D file types**
✔️ **Identify potential Denial-of-Service (DoS) risks**
✔️ **Detect harmful file structures before they reach sensitive systems**

Discovering simple and effective ways to handle these issues was a major win.

Some of the key points that I leaned was about binary and text based data.

## **For binary STLs**
You can canlculate the number of triangles in the file and compare it to the file size. 
it also allows to prevent craches from memory over allocation of mismatched trianle count and actual size

## **For text based data** 
I found that a lot of text based data have similar structres where there is first a keyword,
and data foloing it. This allows for file verification by searching by said keywords, 
and was easily automated in `kwd_search.py`. it also allows for the detection of arbitary data as the keyword found would likelly not match

---

## 🔄 What I'd Improve Next Time

If I were to rebuild this project from scratch, I would focus on:

🛠 **Cleaner Code Structure** → Enhancing readability and making functions easier to navigate and modify.
🛠 **Better Function Organization** → Structuring components to quickly maintenance and intigarte code.

While the project wasn’t fully completed within the three-day timeframe, I plan to continue refining and optimizing it over time.

---

## 🚀 Future Plans

This project **will continue evolving** as needed. Currently, **optimization is minimal**, but any bottlenecks will be addressed as they arise. If additional features or improvements become necessary, they will be implemented based on real-world requirements.

🔹 **Scalability** → Expanding the system when needed.

🔹 **Security** → Strengthening file validation and protection.

🔹 **Workflow Automation** → Making the process faster, and do more.

<br></br>

<br></br>

<br></br>

<br></br>

<br></br>

