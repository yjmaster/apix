from voucher.database.LoadDB import LoadDB
loadDb = LoadDB()
class Util():
    def duplicationCheck(self, params, tableName, colName):
        result = None
        try:
            result = {"success": True}
            loadDb.DB_CONNECT()
            _SQL = "SELECT COUNT(*) as cnt FROM {} WHERE {} = '{}'"\
                .format(tableName, colName, params[colName])

            #print("== CALL SQL ==")
            #print(_SQL)

            with loadDb.conn.cursor() as cursor :
                cursor.execute(_SQL)

            duplicate_cnt = list(cursor)[0][0]
            if duplicate_cnt > 0:
                result["success"] = False
                result["message"] = "{} values ?�​are duplicated".format(colName)

            return result
   
        except Exception as exp:
            result = {"success": False, "message": str(exp)}
        finally:
            loadDb.conn.commit()
            loadDb.conn.close()
            cursor.close()

    def validationCheck(self, params, required):
        response, message = {"success" : True}, ""

        setFormat = list(required.keys())
        getFormat = list(params.keys())        
        requiredKey = (set(setFormat) - set(getFormat))
        
        if len(requiredKey) == 0:
            # required value check
            for idx, keyName in enumerate(required.keys()):
                if required[keyName] is True :
                    if params[keyName] == "":
                        response["success"] = False
                        message += keyName + ", "
                    else :
                        response["params"] = params
                else :
                    if bool(params[keyName] == "") & response["success"]:
                        params[keyName] = required[keyName]
                        response["params"] = params
                    elif params[keyName] is None :
                        params[keyName] = required[keyName]
                    else :
                        response["params"] = params

            if response["success"] is False :
                message = message[:-2]
                response["message"] = (message + " value is required")

        else :
            # required key check
            for idx, keyName in enumerate(requiredKey):
                if required[keyName] is True :
                    response["success"] = False
                    message += keyName + ", "
                else:
                    params[keyName] = required[keyName]
                    response["params"] = params

            if response["success"] is False :
                message = message[:-2]
                response["message"] = (message + " key is required")
        
        return response
