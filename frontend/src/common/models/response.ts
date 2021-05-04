import { IDictionary } from '@/common/types/baseType';

export default class Response {
  private readonly responseData: IDictionary = {};

  constructor(res: IDictionary) {
    this.responseData = res.data;
  }

  public error() {
    if (typeof this.responseData !== 'object') {
      return this.responseData;
    }

    if (this.responseData.status) {
      return null;
    }

    return this.responseData.reason;
  }

  public data() {
    if (!this.responseData.status) {
      return null;
    }

    return this.responseData.data;
  }
}
