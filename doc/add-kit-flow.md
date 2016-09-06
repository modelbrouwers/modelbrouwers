# Flow to add kits as part of the kitreviews app

There are different flows for kitreview-users, and some involve adding new kits
to the database that don't exist yet.

The aim is to keep the flows simple and intuitive for the end-user(s), while
protecting data-integrity and consistency on the developer/content owner end.


## Possible flows an end-user can go through

1.  User arrives at the index page and fills in the form. User enters the search
    parameters and finds the kit he/she is looking for. User either proceeds to
    the detail page to check existing reviews, click the 'add new review' button
    or clicks the 'add review' button on the search results page.

    In both events that a new review is being added, the kit-ID/selection is
    pre-filled in the form since it was derived from the URL.

    The ease of adding a review for an existing kit is high.

2.  User arrives at the index page and fills in the form, with the intention of
    reading existing reviews. There is no kit yet in the database that matches
    the search parameters. The user should see something along the lines of:

       Oops, we don't have this kit in our database! Would you like to add it?

                            +----------------+
                            |    ADD KIT     |
                            +----------------+

    Clicking the button either goes to a `brouwers.kits.views.CreateView` on its
    own dedicated page, or brings up a modal to add the kit.
    The button should take the search parameters with it and pre-fill them to
    reduce the amount of input required from the user.

    Expected call-to-action conversion in this scenario is low - the user has no
    incentive to add kits that don't have the reviews that he/she is looking for.

3.  User completed a kit and wants to add a review for that kit. User proceeds
    to the reviews index page and uses the search form to look for his/her kit.

    The kit does not exist. The user should be presented with the same text/
    buttons/forms as in scenario 2.

    After submitting the kit, there should be a prominent button (or maybe a
    redirect) to add a review for the newly-created kit.

4.  User completed a kit and wants to add a review for that kit. User does not
    want to do a lot of mouseclicks, so he/she refuses to use the search form.
    User goes straight to the 'add review' form.

    The 'add review' form should show the following kit fields, with
    autocomplete where possible:
        * brand
        * scale
        * name
        * boxart
        * kit number
    All fields are required fields. This may be in modal/popup. Upon entering
    the required fields, a search should be made against existing kits. Kits
    that match (brand/scale/kit number) (leave out the empty fields for matching)
    should be suggested to the user. This is a repetition of the search function.
    A light-weight implementation of this is included in the `brouwers.builds` app.

    The user either selects an existing kit, or creates a new one. No duplicates
    w/r to (brand/scale/kit_number) can exist due to unique constraints in the
    db [verify].

    Once the kit is specified, the regular create-review process is completed.
