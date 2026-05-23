import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

import axios from 'axios';

import {
  useEffect,
  useState
} from 'react';

function App() {

  const [cycles, setCycles] = useState([]);
  const [file, setFile] = useState(null);

  // Fetch cycle data
  const fetchCycles = () => {

    axios.get("http://127.0.0.1:8000/api/cycles/")
      .then(response => {

        setCycles(response.data);

      })
      .catch(error => {

        console.log(error);

      });

  };

  useEffect(() => {

    fetchCycles();

  }, []);

  // Upload file
  const uploadFile = () => {

    if (!file) {

      alert("Please select a CSV file");
      return;

    }

    const formData = new FormData();

    formData.append("file", file);
    formData.append("name", file.name);

    axios.post(
      "http://127.0.0.1:8000/api/upload/",
      formData
    )
    .then(response => {

      alert("File uploaded successfully");

      fetchCycles();

    })
    .catch(error => {

      console.log(error);

      alert("Upload failed");

    });

  };

  // Analytics
  const totalCycles = cycles.length;

  const avgRiseTime =
    cycles.reduce((a, b) => a + (b.rise_time || 0), 0)
    / (totalCycles || 1);

  const avgFallTime =
    cycles.reduce((a, b) => a + (b.fall_time || 0), 0)
    / (totalCycles || 1);

  return (

    <div className="container py-5">

      <h1 className="mb-5 text-center">
        Sensor Analytics Dashboard
      </h1>

      {/* Upload Section */}

      <div className="card p-4 mb-5 shadow">

        <h4 className="mb-3">
          Upload CSV Dataset
        </h4>

        <div className="d-flex gap-3">

          <input
            type="file"
            className="form-control"
            onChange={(e) => setFile(e.target.files[0])}
          />

          <button
            className="btn btn-primary"
            onClick={uploadFile}
          >
            Upload
          </button>

        </div>

      </div>

      {/* Statistics */}

      <div className="row mb-5">

        <div className="col-md-4">

          <div className="card text-center shadow p-4">

            <h5>Total Cycles</h5>

            <h2>{totalCycles}</h2>

          </div>

        </div>

        <div className="col-md-4">

          <div className="card text-center shadow p-4">

            <h5>Average Rise Time</h5>

            <h2>{avgRiseTime.toFixed(2)}</h2>

          </div>

        </div>

        <div className="col-md-4">

          <div className="card text-center shadow p-4">

            <h5>Average Fall Time</h5>

            <h2>{avgFallTime.toFixed(2)}</h2>

          </div>

        </div>

      </div>

      {/* Table */}

      <div className="card shadow p-4">

        <h4 className="mb-4">
          Cycle Analytics
        </h4>

        <table className="table table-bordered table-hover">

          <thead className="table-dark">

            <tr>

              <th>Cycle</th>
              <th>Peak Amplitude</th>
              <th>Trough Amplitude</th>
              <th>Rise Time</th>
              <th>Fall Time</th>

            </tr>

          </thead>

          <tbody>

            {cycles.map((cycle, index) => (

              <tr key={index}>

                <td>{cycle.cycle_number}</td>
                <td>{cycle.peak_amplitude}</td>
                <td>{cycle.trough_amplitude}</td>
                <td>{cycle.rise_time}</td>
                <td>{cycle.fall_time}</td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}

export default App;