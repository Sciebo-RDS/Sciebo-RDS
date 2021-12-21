export default {
    install: function (Vue) {
        Vue.prototype.openPopup = async function (service, ctx) {
            let url = decodeURIComponent(service.authorize_url) + "&state=" + service.state;
            ctx.$_popup = window.open(url, "_blank");
            ctx.$root.$emit("showoverlay")

            var checkPopup = setInterval(function () {
                if (ctx.$_popup.closed) {
                    ctx.$store.dispatch("requestUserServiceList");
                    clearInterval(checkPopup);
                    ctx.$root.$emit("hideoverlay");
                }
            }, 250);
        }

        Vue.prototype.parseServicename = function (value) {
            if (typeof value !== "string") return "";
            value = value.replace("port-", "");
            return value.charAt(0).toUpperCase() + value.slice(1);
        }

        Vue.prototype.containsService = function (arr, service) {
            for (const el of arr) {
                if (el.servicename === service.servicename) return true;
            }
            return false
        }

        Vue.prototype.getInformations = function (servicename, services = undefined) {
            if (services === undefined) {
                services = this.servicelist;
            }
            for (const service of services) {
                if (service.servicename == servicename) {
                    return service;
                }
            }
            return undefined;
        }

        Vue.prototype.getService = function (arr, servicename) {
            for (const el of arr) {
                if (el.port === servicename) return el;
            }
            return undefined
        }

        Vue.prototype.equalServices = function (arr, array) {
            // if the other array is a falsy value or
            // compare lengths - can save a lot of time
            if (!array || arr.length != array.length) return false;

            for (const el of arr) {
                if (!this.containsService(array, el)) return false;
            }

            return true;
        }

        Vue.prototype.removeDuplicates = function (arr) {
            let servicelist = []

            for (const service of arr) {
                if (!this.containsService(servicelist, service)) {
                    servicelist.push(service)
                }
            }

            return servicelist
        }

        Vue.prototype.excludeServices = function (array, arr) {
            let product = []
            for (const service of array) {
                if (!this.containsService(arr, service)) {
                    product.push(service)
                }
            }
            return product
        }
    }
}