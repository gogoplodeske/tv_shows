
// See https://aka.ms/new-console-template for more information
//using Newtonsoft.Json.Linq;
//using System.Windows.Forms;
using System;
using System.Net;
using System.Text;
using System.Threading.Tasks;
//using System.Xml;
//using System.Xml.Linq;
using Newtonsoft.Json.Linq;
using System.IO;
using System.Configuration;
using System.Net.Http;
using System.Text.RegularExpressions;
using System.Collections.Generic;

public class HelloWorld
{
    
    public static async Task<int> Main(string[] args)
    {

        string url = string.Format("https://api.tvmaze.com/singlesearch/shows?q={0}", args[0]);
        
        HttpClient client = new HttpClient();
        string res="";
        try
        {
            res = await client.GetStringAsync(url);
        }
        catch (HttpRequestException)
        {
            Environment.Exit(10);
        }
        var Answer = JObject.Parse(res)["id"].ToString();
        var name = JObject.Parse(res)["name"].ToString();
        if (name != args[0])
        {
            Environment.Exit(10);
        }
        string url_eps = string.Format("https://api.tvmaze.com/shows/{0}/episodes", Answer);
        HttpClient client_eps = new HttpClient();
        var res_eps = await client.GetStringAsync(url_eps);
        int sum = 0;
        int c = 0;
        var matchs = Regex.Matches(res_eps.ToString(), @"\bruntime(.+?),");
        foreach (Match m in matchs)
        {
            //Console.WriteLine(m.Groups[1].Value.GetType());
            string eps_len = m.Groups[1].Value.Substring(2);
            int number;
            if (int.TryParse(eps_len, out number))
            {
                //Console.WriteLine(number);
                sum += number;
            }
           
            
            c++;
          
        }
        //sum = int.Parse(matchs.Groups[1].Value);
        Console.WriteLine(sum);
        return sum;
        //Console.WriteLine(c);
        //return sum;

    }
}






