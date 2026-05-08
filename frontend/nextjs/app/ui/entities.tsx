import { EntityListProperties  } from '../lib/definitions';

export default function EntityList({ data }: EntityListProperties) {
    const list_items = data.map(trend =>
        <li key = {trend.entity}>{trend.entity} = {trend.total}</li>
    );

    return (
        <ul>{list_items}</ul>
    );
}