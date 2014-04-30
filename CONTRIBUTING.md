# How to Contribute

`isbntools` has a very small code base, so it is a good project to begin your
adventure in open-source... and it is an app, a lib and a framework at the same
time, so you will find plenty of opportunities to contribute.


## Main Steps

1. Make sure you have a [GitHub account](https://github.com/signup/free)
2. Submit a ticket for your issue or idea,
   on https://github.com/xlcnd/isbntools/issues,
   (if possible wait for some feedback before any serious commitment... :)
3. Fork the repository on GitHub (see https://help.github.com/articles/fork-a-repo)
4. `pip install -r requirements-dev.txt`
5. Do your code... (**remember the code must run on python 2.6, 2.7, 3.3, 3.4, pypy
   and be OS independent**) (you will find `travis-ci.org` very handy for this!)
6. Write tests for your code using `nose` and put then in the directory `isbnools/test`
7. Pass **all tests** and with **coverage > 90%**.
   Check the coverage in [Coveralls](http://bit.ly/1mWwjuE).
8. **Check if all requirements are fulfilled**!
9. Make a pull request on GitHub...
   (see https://help.github.com/articles/using-pull-requests/)


## Style

Your code **must** be PEP8 compliant and be concise as possible (check it with
`flake8` and `pylint`).

Comments should be used only on doc strings or (**very** sparengly) as signposts
for fellow developers. Make your code as clear as possible.


## Red Lines

**Don't submit pull requests that are only comments to the code that is
already in the repo!**
Don't expect kindness if you do that :(.
You could comment and give suggestions on the code at
[issues](http://bit.ly/1i8vmhB) page.

**No** doc tests! Remember point 6 above.

**Don't** submit pull requests without checking point 8!



## Suggestions

Read http://bit.ly/1mctuZk for possible enhancements to the code.
If you have some idea that is not there enter your own.
Select some focused issue and enter some comments on how you plan to tackle it.

See if your code can be written as a pluggin.


## Important

If you don't have experience in these issues, don't be put off by these requirements,
see them as a learning opportunity. Thanks!
