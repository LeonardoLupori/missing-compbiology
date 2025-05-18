# Git basics

## Outline

- [The Basics](#the-basics)
- [The History of git](#the-history-of-git)  


## The Basics

### The Problem Working with Text Data

In neurobiology research, you frequently work with various types of text data:
- Analysis scripts in MATLAB or Python
- Data processing pipelines
- Statistical analysis code
- Notes and documentation
- Configuration files for experimental equipment

#### Keeping Track of Changes

When working on complex analyses or developing new methods, your code evolves constantly. Consider this common scenario:

```
analysis_script.py               # Original script
analysis_script_v2.py            # Added new feature
analysis_script_v2_fixed.py      # Fixed a bug
analysis_script_final.py         # "Final" version
analysis_script_final_FIXED.py   # Actually fixed version
analysis_script_USETHISONE.py    # The truly final version?
```

This approach quickly becomes unmanageable:

```
                     .--.
                    |o_o |    "Which version had the
                    |:_/ |     working spike sorting
                   //   \ \    algorithm again?"
                  (|     | )
                 /'\_   _/`\
                 \___)=(___/
```

#### Being Able to Roll Back to Any Version

During research, you often need to revisit previous approaches:

- "The analysis worked better before I added that normalization step..."
- "We need to compare results with the method we used three months ago..."
- "That function I deleted would actually be useful now..."

Without version control, recovering old work often means:
- Searching through dozens of backup files
- Trying to remember which changes were made when
- Reconstructing code from memory or notes
- Sometimes completely rewriting functionality that was previously working

#### Tracking Collaborative Work

Neurobiology research is increasingly collaborative, involving:
- Multiple lab members working on the same codebase
- Collaborations between labs
- Sharing methods with the broader scientific community

Without a proper system, collaboration becomes chaotic:

- "Did you incorporate my changes to the preprocessing pipeline?"
- "We're both modifying the same files – whose version is correct?"
- "How do we merge our different approaches to the analysis?"
- "How can we work simultaneously without overwriting each other's work?"

### What is a Version Control System?

A Version Control System (VCS) is specialized software designed to track changes to files over time. Git is the most widely used VCS today.

Key features of Git include:

1. **History tracking**: Records the complete history of changes to your files
2. **Branching**: Allows parallel development paths without interference
3. **Merging**: Combines work from different sources automatically
4. **Collaboration**: Facilitates multiple people working on the same codebase
5. **Backup**: Provides distributed copies of the entire project history

```
  Timeline of changes tracked by Git
  
  ●───●───●───●───●───●───● main branch
       \         /
        ●───●──● feature branch
```

### 3. Why Would You Want to Learn to Use One?

For neurobiology researchers, Git provides numerous benefits:

1. **Reproducibility**: The cornerstone of good science is the ability to reproduce results. Git ensures you can recreate the exact code state used for specific analyses or experiments.

2. **Traceability**: Git's detailed history helps you understand why specific changes were made, addressing questions like "Why did we choose this parameter?" or "When did we implement this algorithm?"

3. **Collaboration**: Modern neuroscience often requires interdisciplinary teams. Git allows specialists to work effectively together without confusion.

4. **Code Quality**: Git's branching model encourages testing new approaches without breaking working code, leading to more robust analysis pipelines.

5. **Publication Support**: When publishing your research, Git makes it easier to:
   - Share exact code versions with collaborators and reviewers
   - Maintain open-source research code
   - Meet journal requirements for code availability
   - Document the evolution of methods

6. **Skill Transferability**: Git is an industry-standard tool used across academia, biotech, pharmaceutical research, and tech companies.

7. **Integration with Modern Tools**: Git connects seamlessly with platforms like GitHub, providing additional features like:
   - Issue tracking
   - Automated testing
   - Documentation hosting
   - Publication of datasets and results

In this course, you'll learn how to leverage Git to make your neurobiology research more efficient, collaborative, and reproducible.


## The History of Git

### Why and How Was Git Born?

Git was born out of necessity during the development of the Linux kernel. Before Git, the Linux kernel team used a proprietary version control system called BitKeeper, which they had been using without charge since 2002. However, in April 2005, the relationship between the Linux development community and BitKeeper's commercial developer deteriorated when BitKeeper revoked the free license.

This crisis forced the Linux kernel community, particularly Linus Torvalds, to develop their own version control system. Torvalds had several specific requirements:

- **Speed**: The system needed to be extremely fast to handle the large codebase of the Linux kernel
- **Distributed workflow**: Unlike centralized systems, developers needed to work independently
- **Safeguards against corruption**: The system needed strong mechanisms to ensure data integrity
- **Simple design**: The architecture needed to be understandable and maintainable

Torvalds took a short break from kernel development and created Git in just a few weeks in April 2005. The name "Git" is British English slang that can mean an unpleasant or stubborn person - Torvalds joked that he names his projects after himself.

```
April 3, 2005: BitKeeper license revoked
             |
             v
April 7, 2005: Git development begins
             |
             v
April 29, 2005: Git self-hosts (used to manage its own source code)
             |
             v
June 16, 2005: Git manages Linux kernel v2.6.12
```

### Who Is the Inventor?

Linus Torvalds, the creator of the Linux kernel, is the original inventor of Git. After the initial development period, Torvalds handed over maintenance of Git to Junio Hamano, who has been the primary maintainer since July 2005 and continues in this role today.

Torvalds is known for his pragmatic and sometimes controversial approach to software development. When creating Git, he focused on solving his immediate problem (managing Linux kernel development) rather than creating a tool for general use. Despite this narrow initial focus, Git's design principles proved to be broadly applicable, leading to its widespread adoption.

```
          .--.
         |o_o |
         |:_/ |    "I'm an egotistical bastard,
        //   \ \    so I name all my projects after myself.
       (|     | )   First Linux, now Git."
      /'\_   _/`\         - Linus Torvalds
      \___)=(___/
```

### Alternatives to Git

While Git has become the dominant version control system, several alternatives exist, each with different strengths:

1. **Mercurial (Hg)**: Created around the same time as Git, also in response to the BitKeeper situation. Mercurial is known for its simplicity and ease of use. It's used by organizations like Mozilla and Facebook (for the main Facebook codebase).

2. **Subversion (SVN)**: A centralized version control system that was very popular before Git. Some organizations still use SVN for specific use cases, though many have migrated to Git.

3. **Perforce (Helix Core)**: A commercial, centralized version control system that handles large binary files well. Used in game development and industries with large non-text assets.

4. **Fossil**: An integrated bug tracking, wiki, and version control system in a single package, created by the SQLite team.

5. **Bazaar**: A distributed version control system that was backed by Canonical (the company behind Ubuntu) but is now less actively developed.

```
Version Control System Evolution:

RCS (1982) --> CVS (1990) --> Subversion (2000) --+
                                                   |
BitKeeper (2000) -------------------------+        |
                                          |        |
                                          v        v
                                     Git (2005)  Mercurial (2005)
```

### Why Do We Mainly Cover Git?

In this course, we focus on Git for several compelling reasons:

1. **Industry Standard**: Git has become the de facto standard for version control in both industry and academia. According to Stack Overflow's 2023 Developer Survey, over 90% of developers use Git.

2. **GitHub/GitLab Ecosystem**: Git integrates with platforms like GitHub and GitLab, which provide additional collaboration features crucial for research:
   - Issue tracking for experiment planning
   - Pull requests for code review
   - CI/CD for automated testing
   - Wikis for documentation

3. **Distributed Nature**: Git's distributed architecture allows neurobiology researchers to work offline in lab environments that may have limited connectivity, while still maintaining a complete history.

4. **Branching Capabilities**: Git's lightweight branching is ideal for experimental research where you might pursue multiple analytical approaches in parallel.

5. **Large Community**: The vast Git user base means abundant resources, tutorials, and solutions to common problems.

6. **Cross-platform**: Git works consistently across Windows, macOS, and Linux, supporting the diverse computing environments found in neurobiology research.

7. **Future-proofing**: Learning Git provides researchers with a skill that will remain relevant throughout their careers, regardless of whether they stay in academia or move to industry.

While other version control systems have their merits, Git's ubiquity and extensive ecosystem make it the most valuable system to learn for neurobiology researchers who want their work to be accessible, collaborative, and aligned with current best practices in scientific computing.





