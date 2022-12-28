package ipca.budget.smartenergy.data

import android.util.Log
import ipca.budget.smartenergy.data.model.LoggedInUser
import java.io.IOException
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject

/**
 * Class that handles authentication w/ login credentials and retrieves user information.
 */
class LoginDataSource {
    val loginmethod = "login"
    //val server = "10.10.10.2"  // raspberry pi - real test
    val server = "192.168.1.40"  // home office tests
    private val client = OkHttpClient()

    fun login(username: String, password: String): Result<LoggedInUser> {
        try {
            // TODO: handle loggedInUser authentication
            println("###########################################")
            println("#### LOGIN")
            var url = "http://" + server + ":80/login.php?method=" + loginmethod + "&username=" + username + "&password=" + password

            val request = Request.Builder().url(url).build()
            println("#### val request... " + request.toString())
            println("#### client.newCall...")
            Log.v(TAG,"#### Teste")
            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) throw IOException("Unexpected code $response")
                for ((name, value) in response.headers) {
                    println("$name: $value")
                }
                println(response.body!!.string())
                println("#### response")
            }

            val idUser = 1
            val loggedUser = LoggedInUser("1", "Test")
            println("#### user logged in : "+ idUser + " " + username)
            return Result.Success(loggedUser)
        } catch (e: Throwable) {
            println("#### login error : " + e.message)
            return Result.Error(IOException("Error logging in", e))
        }
    }

    fun logout() {
        // TODO: revoke authentication
    }

    companion object {
        private const val TAG ="############ Mensagens..."
    }
}

