class Paginator {
  constructor() {
    this.paginate_by = null;
    this.page_range = [];
    this.previous_page_number = null;
    this.next_page_number = null;
    this.number = null;
    this.next = null;
    this.previous = null;
  }

  /* checks if an api response can be paginated, and does so if possible */
  paginate(response, page) {
    if (response.count === undefined) {
      return;
    }
    page = page || 1;

    this.paginate_by = response.paginate_by;
    this.next = response.next;
    this.previous = response.previous;
    this.number = page;

    if (response.results.length > 0) {
      var n = Math.ceil(response.count / this.paginate_by);
      for (let i = 1; i <= n; i++) {
        this.page_range.push(i);
      }
    }

    var index = this.page_range.indexOf(this.number);
    this.previous_page_number = this.page_range[index - 1] || null;
    this.next_page_number = this.page_range[index + 1] || null;
  }

  get has_previous() {
    return this.previous_page_number !== null;
  }

  get has_next() {
    return this.next_page_number !== null;
  }
}

export default Paginator;
