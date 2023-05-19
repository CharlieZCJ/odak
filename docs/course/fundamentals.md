# Fundamentals and Standards


This chapter will review some background information you will likely use in the rest of this course.
In addition, we will also introduce you to a structure where we establish some standards to decrease the chances of producing buggy or incompatible codes.


## Required Production Environment :material-alert-decagram:{ .mdx-pulse title="Too important!" }


:octicons-info-24: Informative ·
:octicons-beaker-24: Practical


We have provided some information in [prerequisites](index.md).
This information includes programming language requirements, required libraries, text editors, build environments, and operating system requirements.
For installing our library, odak, we strongly advise using the version in the source repository.
You can install odak from the source repository using your favorite terminal and operating system:


```shell
pip3 install git+https://github.com/kaanaksit/odak
```

Note that your production environment meaning your computer and required software for this course is important.
To avoid wasting time in the next chapters and get the most from this lecture, please ensure that you have dedicated enough time to set everything up as it should.


## Production Standards :material-alert-decagram:{ .mdx-pulse title="Too important!" }


:octicons-info-24: Informative


In this course, you will be asked to code and implement phenomena related to the physics of light.
Your work, meaning your production, should strictly follow certain habits to help build better tools and developments.


### Subversion and Revision Control


:octicons-info-24: Informative ·
:octicons-beaker-24: Practical


As you develop your code for your future homework and projects, you will discover that many things could go wrong.
For example, the hard drive that contains the only copy of your code could be damaged, or your most trusted friend (so-called) can claim that she compiled most of the work, although that is not the case.
These are just a few cases that may happen in your case.
Poor code control can cause companies to lose money by releasing incorrect codes or researchers to lose their reputations as their work is challenging to replicate.
_How do you claim in that case that you did your part?_
_What is the proper method to avoid losing data, time, effort, and motivation?_


This is where the subversion, authoring, and revision control systems come in for the example cases discussed in the previous paragraph.
In today's world, [Git](https://git-scm.com/) is a widespread version control system adopted by major websites such as [GitHub](https://github.com/) or [Gitlab](https://about.gitlab.com/).
We will not dive deep into how to use Git and all its features, but I will try to highlight parts that are likely essential for your workflow.
I encourage you to **use Git** for creating a repository for every one of your tasks.
You can either keep this repository in your locally and constantly back up somewhere else or use these online services such as [GitHub](https://github.com/) or [Gitlab](https://about.gitlab.com/).
I also encourage you to use the online services if you are a beginner.


For each operating system, installing Git has its own processes, but for an Ubuntu operating system, it is as easy as typing the following commands in your terminal:

```shell
sudo apt install git
```

Let us imagine that you want to start a repository on GitHub.
Make sure to create a private repository, and please only go public with any repository once you feel it is at a state where it can be shared with others.
Once you have created your repository on GitHub, you can clone the repository using the following command in a terminal:


```shell
git clone REPLACEWITHLOCATIONOFREPO
```


You can find out about the repository's location by visiting the repository's website that you have created.
The location is typically revealed by clicking the code button, as depicted in the below screenshot.


<figure markdown>
  ![Image title](media/git_clone.png){ width="600" }
  <figcaption>A screenshot showing how you can acquire the link for cloning a repository from GitHub.</figcaption>
</figure>


For example, in the above example case, the command should be updated with the following:

```shell
git clone git@github.com:kaanaksit/odak.git
```

If you want to share your private repository with someone you can go into the settings of your repository in its webpage and navigate to the collaborators section.
This way, you can assign roles to your collaborators that best suits your scenario.

!!! warning end "Secure your account"
    If you are using GitHub for your development, I highly encourage you to consider using [two-factor authentication](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa).

#### Git Basics
:octicons-info-24: Informative ·
:octicons-beaker-24: Practical

If you want to add new files to your subversion control system, use the following:

```shell
git add YOURFILE.jpeg
```

And later, you can update the online copy (remote server or source) using the following:

```shell
git commit -am "Explain what you add in a short comment."
git push
```

In some cases, you may want to include large binary files in your project, such as a paper, video, or any other media you want to achieve within your project repository.
For those cases, using just `git` may not be the best opinion, as Git works on creating a history of files and how they are changed at each commit, this history will likely be too bulky and oversized.
Thus, cloning a repository could be really slow when large binary biles and Git come together.
Assuming you are on an Ubuntu operating system, you can install the [Large File Support (LFS)](https://git-lfs.com/) for Git by typing these commands in your terminal:


```shell
sudo apt install git-lfs
```

Once you have the LFS installed in your operating system, you can then go into your repository and enable LFS:

```shell
cd YOURREPOSITORY
git lfs install
```

Now is the time to let your LFS track specific files to avoid overcrowding your Git history.
For example, you can track `*.pdf` extension, meaning all the PDF files in your repository by typing the following command in your terminal:

```shell
git lfs track *.pdf
```

Finally, ensure the tracking information and LFS are copied to your remote/source repository. 
You can do that using the following commands in your terminal:

```shell
git add .gitattributes
git commit -am "Enabling large file support."
git push
```


## Coding Standards :material-alert-decagram:{ .mdx-pulse title="Too important!" }


:octicons-info-24: Informative ·
:octicons-beaker-24: Practical


I encourage our readers to follow the methods of coding highlighted here.
Following the methods that I am going to explain is not only crucial for developing replicable projects, but it is also vital for allowing other people to read your code with the least amount of hassle.

### Avoid using long lines.
Please avoid having too many characters in one line.
Let us start with a bad example:

```python
def light_transport(wavelength, distances, resolution, propagation_type, polarization, input_field, output_field, angles):
      pass
      return results
```

As you can observe, the above function requires multiple inputs to be provided.
Try making the inputs more readable by breaking lines and in some cases, you can also provide the requested type for an input and a default value to guide your users:


```python
def light_transport(
                    wavelength,
                    distances,
                    resolution,
                    propagation_type : str, 
                    polarization = 'vertical',
                    input_field = torch.rand(1, 1, 100, 100),
                    output_field = torch.zeros(1, 1, 100, 100),
                    angles= [0., 0., 0.]
                   ):
    pass
    return results
```

### Leave spaces between commands, variables and functions

Please avoid writing code like a train of characters.
Here is a terrible coding example:

```python
def addition(x,y,z):
    result=2*y+z+x**2*3
    return result
```

Please leave spaces after each comma, `,`, and mathematical operation.
So now, we can correct the above example as in below:

```python
def addition(x, y, z):
    result = 2 * y + z + x ** 2 * 3
    return result
```

Please also leave two lines of space between the two functions.
Here is a bad example again:

```python
def add(x, y):
    return x + y
def multiply(x, y):
    return x * y
```

Instead, it should be:


```python
def add(x, y):
    return x + y


def multiply(x, y):
    return x * y
```


### Add documentation
For your code, please make sure to add the necessary documentation.
Here is a good example of doing that:


```python
def add(x, y):
    """
    A function to add two values together.

    Parameters
    ==========
    x         : float
                First input value.
    y         : float
                Second input value.

    Returns
    =======
    result    : float
                Result of the addition.
    """
    result = x + y
    return result
```


### Use code style checker and validator
There are also code-style checkers and code validators that you can adapt to your workflows when coding.
One of these code-style checkers and validators I use in my projects is `pyflakes.`
On an Ubuntu operating system, you can install `pyflakes` easily by typing these commands into your terminal:


```shell
sudo apt install python3-pyflakes
```


It could tell you about missing imports or undefined or unused variables.
You can use it on any Python script very easily:

```shell
pyflakes3 sample.py
```


In addition, I use `flake8` and `autopep8` for standard code violations.
To learn more about these, please read the [code section of the contribution guide](../contributing/#code).


### Fixing bugs
Often, you can encounter bugs in your code.
To fix your code in such cases, I would like you to consider using a method called `Rubber duck debugging` or `Rubber ducking.`
The basic idea is to be able to express to a third person or yourself code line by line.
Explaining line by line could help you see what is wrong with your code.
I am sure there are many recipes for solving bugs in codes.
I tried introducing you to one that works for me.


## Background Review :material-alert-decagram:{ .mdx-pulse title="Too important!" }


:octicons-info-24: Informative


### Convolution Operation


### Gradient Descent Optimizers


## Conclusion


??? tip end "Consider revisiting this chapter"
    Remember that you can always revisit this chapter as you progress with the course as you need it.
    This chapter is vital for establishing a means to complete your assignments and could help formulate a suitable base to collaborate and work with [my research group](https://complightlab.com) and other experts in the field.
