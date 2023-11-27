import { useState } from 'react'
import DB_Logic from './DB_Logic'

function App() {

  return (
      <div className="h-full w-full bg-slate-500">
        <div className="navbar bg-neutral text-neutral-content">
          <button className="btn btn-ghost text-xl text-white mx-auto">LinkedIn Job Statistics Ireland</button>
        </div>
        <div>
          <DB_Logic />
        </div>
      </div>
  )
}

export default App
