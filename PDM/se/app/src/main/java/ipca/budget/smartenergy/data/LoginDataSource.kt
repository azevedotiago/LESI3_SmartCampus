package ipca.budget.smartenergy.data

import ipca.budget.smartenergy.data.model.LoggedInUser
import java.io.IOException
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import java.net.ResponseCache


/**
 * Class that handles authentication w/ login credentials and retrieves user information.
 */
class LoginDataSource {
    val loginmethod = "login"
    //val server = "10.10.10.2"
    val server = "192.168.1.40" // home office tests
    private val client = OkHttpClient()

    fun login(username: String, password: String): Result<LoggedInUser> {
        try {
            // TODO: handle loggedInUser authentication
            println("###########################################")
            println("### LOGIN")
            println("### username : " + username)
            println("### password : " + password)
            var url = "http://" + server + ":80/login.php?method=" + loginmethod + "&username=" + username + "&password=" + password
            println("### url      : " + url)

            println("### result  : fetching...")
            val request = Request.Builder().url(url).build()
            println("### val request... " + request.toString())


            println("### 1 client.newCall...")
            client.newCall(request).execute().use { response : Response ->
                if (!response.isSuccessful) throw IOException("Unexpected code $response")

                //for ((name, value) in response.headers) {
                //    println("$name: $value")
                //}

                //println(response.body!!.string())
                println("### response")
            }
            val fakeUser = LoggedInUser(java.util.UUID.randomUUID().toString(), "Jane Doe")
            println("### fakeUser")
            return Result.Success(fakeUser)
        } catch (e: Throwable) {
            println("### login: error 1: " + e.message)
            return Result.Error(IOException("Error logging in", e))
        }
    }
    fun logout() {
        // TODO: revoke authentication
    }
}