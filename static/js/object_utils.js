var _API_URL = "http://211.232.77.118:10001";
//var _API_URL = "http://127.0.0.1:5000";

var config = {
  contextPath : '',
  datetimeFormat : 'YYYY-MM-DD',
  dateFormat : 'YYYY-MM-DD'
};

$.widget("custom.datepicker", {
  options: {
    type: 'range', // single || range
    picker: null,
    hiddenId: null,
    hiddenName: null,
    minDate: null,
    maxDate: null
  },
  _create: function () {
    if (ObjectUtils.isEmpty($(this.element).attr("id"))) {
      console.error(this.element, "ID 값을 넣어 주세요");
      return false;
    }
    if (ObjectUtils.isEmpty($(this.element).attr("name"))) {
      console.error(this.element, "name 값을 넣어 주세요");
      return false;
    }
    this._initUI();
    this._createDatePick();
    this._appendHiddenFiled();
  },
  _createDatePick: function () {
    $(this.element)
    .attr("readonly", "readonly")
    .attr("placeholder", "날짜를 입력하세요.")
    .addClass("form-control ml5 pointer date_input")
    .css("background-color", "#fff");
  },
  _appendHiddenFiled: function () {
    this.options.hiddenId = $(this.element).attr("id") || "date_picker_id";
    this.options.hiddenName = $(this.element).attr("name")
        || "date_picker_name";

    $(this.element)
    .after(
        "<input type=\"hidden\" id=\"" + this.options.hiddenId + "_to\" name=\""
        + this.options.hiddenName + "_to\" />")
    .after("<input type=\"hidden\" id=\"" + this.options.hiddenId
        + "_from\" name=\"" + this.options.hiddenName + "_from\" />");
  },
  _initUI: function () {
    var self = this;
    this.options.picker = new lightPick({
      field: $(this.element)[0],
      singleDate: this.options.type == "single" ? true : false,
      minDate : this.options.minDate,
      maxDate : this.options.maxDate,
      firstDay: 0,
      numberOfMonths: this.options.type == "single" ? 1 : 2,
      lang: 'ko',
      format: config.dateFormat,
      separator: ' ~ ',
      autoclose: true,
      hideOnBodyClick: true,
      footer: this.options.type == "single" ? false
          : '<button type="button" class="lightpick__reset-action">초기화</button>',
      locale: {
        buttons: {
          prev: '←',
          next: '→',
          close: '×'
        },
        tooltip: {
          one: '일',
          other: '일'
        },
        tooltipOnDisabled: null,
        pluralize: function (i, locale) {
          if (typeof i === "string") {
            i = parseInt(i, 10);
          }

          if (i === 1 && 'one' in locale) {
            return locale.one;
          }
          if ('other' in locale) {
            return locale.other;
          }

          return '';
        }
      },
      onOpen: function () {
        $("#" + self.options.hiddenId + "_from").val("");
        $("#" + self.options.hiddenId + "_to").val("");
      },
      onClose: function () {
        if (ObjectUtils.isNotEmpty(this.getStartDate())) {
          if (self.options.type == "range") {
            $("#" + self.options.hiddenId + "_from").val(
                this.getStartDate().format("YYYY.MM.DD") + " 00:00:00");
            if (ObjectUtils.isNotEmpty(this.getEndDate())) {
              $("#" + self.options.hiddenId + "_to").val(
                  this.getEndDate().format("YYYY.MM.DD") + " 23:59:59");
            } else {
              $("#" + self.options.hiddenId + "_to").val("");
            }
          } else {
            $("#" + self.options.hiddenId + "_from").val(
                this.getStartDate().format("YYYY.MM.DD") + " 00:00:00");
            $("#" + self.options.hiddenId + "_to").val(
                this.getStartDate().format("YYYY.MM.DD") + " 23:59:59");
          }
        }
        if(sessionStorage.getItem("filter") == 'photo'){
          appPhoto.datepickerCloseEvent();
        }
      }
    });
  },
  setDate: function (date) {
    var self = this;
    self.options.picker.setDate(date);
    $("#" + this.options.hiddenId + "_from").val(date + " 00:00:00");
    $("#" + this.options.hiddenId + "_to").val(date + " 23:59:59");
  },
  setDateRange: function (from, to) {
    var self = this;
    self.options.picker.setDateRange(from, to);
    $("#" + this.options.hiddenId + "_from").val(from + " 00:00:00");
    $("#" + this.options.hiddenId + "_to").val(to + " 23:59:59");
  }
});

var ObjectUtils = {
  // 값의 유무 체크
  isEmpty : function(val) {
    var self = this;
    if (val === undefined) return true;
    if (typeof (val) == 'function' || typeof (val) == 'number' || typeof (val) == 'boolean' || Object.prototype.toString.call(val) === '[object Date]')
      return false;
    if (typeof (val) == 'object') {
      var flag = true;
      for (var f in val) {
        flag = false;
      }
      return flag;
    }
    if (null == val || null === val || "" == val || val == undefined || typeof(val) == undefined || "undefined" == val || "NaN" == val || "null" == val) {
      return true;
    } else {
      return false;
    }
  },
  // 값의 유무 체크
  isNotEmpty: function (val) {
    var self = this;
    return !this.isEmpty(val);
  }
};

String.prototype.string = function (len) { var s = ''; var i = 0; while (i++ < len) { s += this } return s }
String.prototype.zf = function (len) { return '0'.string(len - this.length) + this }
Number.prototype.zf = function (len) { return this.toString().zf(len) }

Date.prototype.getToday = function (day=0, fmt) {
  let redate = this.setDate(this.getDate() + day)
  return new Date(redate).format(fmt);
}

Date.prototype.getWeeks = function (week, fmt) {
  let redate = this.setDate(this.getDate() + (week*6))
  return new Date(redate).format(fmt);
}

Date.prototype.getMonths = function (month, fmt) {
  let redate = this.setMonth(this.getMonth() + (month));
  return new Date(redate).format(fmt);
}

Date.prototype.getYears = function (year, fmt) {
  let redate = this.setFullYear(this.getFullYear() + (year))
  return new Date(redate).format(fmt);
}

Date.prototype.addHours = function (h) {
  this.setHours(this.getHours() + h)
  return this
}

Date.prototype.format = function (f) {
  if (!this.valueOf()) return ' '

  const weekName = ['일요일', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일']
  const d = this.addHours(0)
  if(f === undefined){ f = 'yyyy-MM-dd'; }
  return f.replace(/(yyyy|yy|MM|dd|E|hh|mm|ss|a\/p|l)/gi, function ($1) {
    switch ($1) {
      case 'yyyy': return d.getFullYear()
      case 'yy': return (d.getFullYear() % 1000).zf(2)
      case 'MM': return (d.getMonth() + 1).zf(2)
      case 'dd': return d.getDate().zf(2)
      case 'E': return weekName[d.getDay()]
      case 'HH': return d.getHours().zf(2)
      case 'hh': return ((h = d.getHours() % 12) ? h : 12).zf(2)
      case 'mm': return d.getMinutes().zf(2)
      case 'ss': return d.getSeconds().zf(2)
      case 'l': return d.getMilliseconds().zf(3)
      case 'a/p': return d.getHours() < 12 ? '오전' : '오후'
      default: return $1
    }
  })
}

var common = {
  proxy : function(path, params, multi=true){
      return new Promise(function(resolve, reject) {
          $.ajax({
			url:_API_URL+ "/esg/selectNews",
			type: 'POST',
			crossDomain: true,
			contentType: "application/json; charset=UTF-8",
			headers: {
				"X-Requested-With": "XMLHttpRequest",
				"Access-Control-Allow-Origin" : "*"
			},
			dataType: "json",
			data: JSON.stringify(params),
			beforeSend: function(xhr){
			if(multi){
				$.blockUI({ message: null,  baseZ: 9999 });
			}
			},
			success: function(res){
			if(res["success"]){
				
				resolve(res);
				
			}else{
				alert(res["message"]);
			}
			},
			complete: function () {
				if(multi){$.unblockUI()}
			}
          }).fail(function (e) {
              reject(JSON.stringify(e))
              $.unblockUI();
          });
      });
  },
  proxyAll : function(proxyList, callback){
      $.blockUI({ message: null,  baseZ: 9999 });
      return Promise.all(proxyList).then(values => {
          $.unblockUI();
          callback(values);
      });
  }
}





