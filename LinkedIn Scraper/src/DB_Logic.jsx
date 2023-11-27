import React from 'react';
import { useState, useEffect } from 'react';
import { createClient } from '@supabase/supabase-js'


const DB_Logic = () => {
  const [keyword_Data, setkeyword_Data] = useState([]);
  const [job_Data, setjob_Data] = useState([]);

  // Create a single supabase client for interacting with your database
  const supabase = createClient(import.meta.env.VITE_SUPABASE_URL, import.meta.env.VITE_SUPABASE_PASSWORD)
  const fetchDataKeywords = async () => {
  const twentyFourHoursAgo = new Date();
  twentyFourHoursAgo.setHours(twentyFourHoursAgo.getHours() - 24);
    try {
      const { data,error } = await supabase.from('Daily_Keywords').select().gt('Date', twentyFourHoursAgo.toISOString());;
      setkeyword_Data(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const fetchDataJobs = async () => {
    try {
        const date = new Date();
        let day = date.getDate();
        let month = date.getMonth() + 1;
        let year = date.getFullYear();

        // This arrangement can be altered based on how we want the date's format to appear.
        let currentDate = `${year}-${month}-${day}`;
      const { data,error } = await supabase.from('LinkedIN_Job').select().eq('Date',currentDate);
      setjob_Data(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const countOccurrences = (arr) => {
    return arr.reduce((acc, job) => {
      const JobTitle = job.Job_Title
      acc[JobTitle] = (acc[JobTitle] || 0) + 1;
      return acc;
    }, {});
  };

  const jobOccurrences = countOccurrences(job_Data);
  console.log(jobOccurrences)


  // Use useEffect to call the asynchronous function when the component mounts
  useEffect(() => {
    fetchDataKeywords();
    fetchDataJobs();
  }, []);

  return (
    <div className="bg-white w-full h-full grid grid-cols-2 gap-5 text-black p-5">
      <div className="overflow-x-auto">
        <h1 className="text-black text-xl">Keyword Counts Past 24 Hours</h1>
        <div className="divider p-1 before:bg-black after:bg-slate-500"></div>
        <table className="table">
            <thead>
            <tr>
                <th></th>
                <th className="text-lg text-black">Keyword</th>
                <th className="text-lg text-black">Count</th>
            </tr>
            </thead>
            <tbody>
            {keyword_Data.map((keywords) => (
                <tr key={keywords.id}>
                    <td> </td>
                    <td>{keywords.Keyword}</td>
                    <td>{keywords.Count}</td>
                </tr>
                ))}
            </tbody>
        </table>
        </div>
        <div>
            <h1 className="text-black text-xl">Job Counts Past 24 Hours</h1>
            <div className="divider p-1 before:bg-black after:bg-slate-500"></div>
            <ul>
            {Object.entries(jobOccurrences).map(([job, count]) => (
              <li key={job}>
              {job}: {count}
          </li>
        ))}
            </ul>

        </div>
    </div>
  );
};

export default DB_Logic;