import { EntityListProperties  } from '../lib/definitions';

export default function TrendBar({ data }: EntityListProperties) {
    const maxTotal = Math.max(...data.map(trend => trend.total)) * 1.25;

    const listItems = data.map(trend => 
        	
        <div key = {trend.entity} className = "grid gap-6 grid-cols-[180px_1fr_auto] ">
            <span className = "capitalize">{trend.entity}</span>        
            <div className="mb-5 h-4 overflow-hidden rounded-full bg-gray-200"> {/* This is the background bar */}
                <div className="h-4 rounded-full bg-gradient-to-r from-purple-500 to-blue-300" style = {{ width: `${(trend.total / maxTotal) * 100}%` }}></div> {/* We are capping the max bar at 80% width.*/}
            </div>
            <span>{trend.total}</span>
       </div>
    );

    return (
        <div>
            {listItems}
        </div>
    );
}